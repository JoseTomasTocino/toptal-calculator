import logging
import math

from calculator import tokens
from calculator.parser import tokenize, infix_to_postfix

logger = logging.getLogger(__name__)


class EquationNode:
    def __init__(self, coefficient=None, constant=None):
        self.coefficient = coefficient
        self.constant = constant

    def has_constant(self):
        return self.constant is not None

    def has_coef(self):
        return self.coefficient is not None

    def __str__(self):
        return "[EquationNode, coeff = {}, constant = {}]".format(self.coefficient, self.constant)

    def __repr__(self):
        return self.__str__()


def evaluate(input, is_postfix=False):
    input = input.strip()
    if not input:
        raise RuntimeError("Missing expression")

    logger.debug("Evaluating input '%s'", input)

    token_list = tokenize(input)

    logger.debug("Tokens:")
    for tok in token_list:
        logger.debug("    %r", tok)

    # Decide whether it's an expression or an equation
    is_equation = False

    # For equations, convert the equal sign into a "minus" sign and surround the RHS of the equation in parenthesis
    for i, tok in enumerate(token_list):
        if isinstance(tok, tokens.EqualSignToken):
            logger.debug("Detected equation")
            is_equation = True
            token_list.pop(i)
            token_list.insert(i, tokens.MinusOperatorToken())
            token_list.insert(i + 1, tokens.OpenParenthesisToken())
            token_list.append(tokens.CloseParenthesisToken())
            break

    # Equation testing
    if is_equation:

        # Make sure there are variables if it's an equation
        for i, tok in enumerate(token_list):
            if isinstance(tok, tokens.VariableToken):
                break
        else:
            raise RuntimeError("Incorrect equation: missing variable")

        # Make sure there are no more equal signs
        if len([x for x in token_list if isinstance(x, tokens.EqualSignToken)]):
            raise RuntimeError("Incorrect equation: more than one equal sign found")

        # Make sure all variables are the same
        if len(set([x.value for x in token_list if isinstance(x, tokens.VariableToken)])) > 1:
            raise RuntimeError("Only one variable allowed")

    # Make sure there are no variables if it's not an equation
    if not is_equation:
        for i, tok in enumerate(token_list):
            if isinstance(tok, tokens.VariableToken):
                raise RuntimeError("Variable '{}' found in non-equation".format(tok.value))

    if not is_postfix:
        logger.debug("Converting to postfix")
        token_list = infix_to_postfix(token_list)

    logger.debug("Tokens in postfix:")
    for tok in token_list:
        logger.debug("    %r", tok)

    stack = []
    logger.debug("Evaluating token list:")
    for tok in token_list:
        logger.debug("")
        logger.debug("Stack: %r", stack)
        logger.debug("%r", tok)

        node = None

        if tokens.is_operand(tok):
            node = EquationNode(constant=tok.value)

        elif tokens.is_variable(tok):
            node = EquationNode(coefficient=1)

        elif tokens.is_constant(tok):
            node = EquationNode(constant=tok.value)

        else:
            if tokens.is_operator(tok):
                try:
                    second_operand = stack.pop()
                    first_operand = stack.pop()

                except IndexError:
                    raise RuntimeError("Bad expression, missing operands")

                logger.debug("  Oper A: %r", first_operand)
                logger.debug("  Oper B: %r", second_operand)

                if isinstance(tok, tokens.PlusOperatorToken):
                    constant = 0
                    coefficient = 0

                    if first_operand.constant is not None:
                        constant = first_operand.constant

                    if second_operand.constant is not None:
                        constant += second_operand.constant

                    if constant == 0:
                        constant = None

                    if first_operand.coefficient is not None:
                        coefficient = first_operand.coefficient

                    if second_operand.coefficient is not None:
                        coefficient += second_operand.coefficient

                    if coefficient == 0:
                        coefficient = None

                    node = EquationNode(coefficient=coefficient, constant=constant)

                elif isinstance(tok, tokens.MinusOperatorToken):
                    constant = 0
                    coefficient = 0

                    if first_operand.constant is not None:
                        constant = first_operand.constant

                    if second_operand.constant is not None:
                        constant -= second_operand.constant

                    if constant == 0:
                        constant = None

                    if first_operand.coefficient is not None:
                        coefficient = first_operand.coefficient

                    if second_operand.coefficient is not None:
                        coefficient -= second_operand.coefficient

                    if coefficient == 0:
                        coefficient = None

                    node = EquationNode(coefficient=coefficient, constant=constant)

                elif isinstance(tok, tokens.ProductOperatorToken):
                    constant = None
                    coefficient = None

                    if first_operand.has_constant():
                        if second_operand.has_constant():
                            if constant is None: constant = 0
                            constant += first_operand.constant * second_operand.constant

                        if second_operand.has_coef():
                            if coefficient is None: coefficient = 0
                            coefficient += first_operand.constant * second_operand.coefficient

                    if first_operand.has_coef():
                        if second_operand.has_constant():
                            if coefficient is None: coefficient = 0
                            coefficient += first_operand.coefficient * second_operand.constant

                        if second_operand.has_coef():
                            raise RuntimeError("Unsupported expression, can't have exponential variables")

                    node = EquationNode(coefficient=coefficient, constant=constant)

                elif isinstance(tok, tokens.DivisionOperatorToken):
                    constant = None
                    coefficient = None

                    if first_operand.has_constant():
                        if second_operand.has_constant():
                            if constant is None: constant = 0
                            constant += first_operand.constant / second_operand.constant

                        if second_operand.has_coef():
                            raise RuntimeError("Unsupported expression, non-linear equations are not supported")

                    if first_operand.has_coef():
                        if second_operand.has_constant():
                            if coefficient is None: coefficient = 0
                            coefficient += first_operand.coefficient / second_operand.constant

                        if second_operand.has_coef():
                            raise RuntimeError("Unsupported expression, can't have exponential variables")

                    node = EquationNode(coefficient=coefficient, constant=constant)

            elif tokens.is_function(tok):
                try:
                    operand = stack.pop()

                except IndexError as e:
                    raise RuntimeError("Missing value for trigonometric function")

                # Functions are only allowed in simple expressions, not in equations, so there should be no coeffs.
                if operand.has_coef():
                    raise RuntimeError("Function not allowed in equations")

                # Make sure there's a value to work with
                if not operand.has_constant():
                    raise RuntimeError("Missing value for trigonometric function")

                if tokens.is_trigonometric(tok):
                    node = EquationNode(constant=tok.oper(operand.constant))

                elif isinstance(tok, tokens.LnFunctionToken):
                    node = EquationNode(constant=math.log(operand.constant, math.e))

                elif isinstance(tok, tokens.LogFunctionToken):
                    base = 10

                    if tok.has_custom_base:
                        base = stack.pop().constant

                    node = EquationNode(constant=math.log(operand.constant, base))

        if node is not None:
            logger.debug("Pushing to stack: %r", node)
            stack.append(node)

    logger.debug("Final stack %r", stack)

    arred = lambda x, n: x * (10 ** n) // 1 / (10 ** n)

    logger.info("Input: {}".format(input))

    if is_equation:
        value = -stack[-1].constant / stack[-1].coefficient
        value = arred(value, 10)
        logger.info("x = {}".format(value))

    else:
        value = stack[-1].constant
        value = arred(value, 10)
        logger.info(value)

    return value
