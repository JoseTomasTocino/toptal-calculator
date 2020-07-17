import logging
import math

from calculator.parser.tokenizer import tokenize, infix_to_postfix
from calculator.parser.tokens import EqualSignToken, OperandToken, is_variable, MinusOperatorToken, \
    OpenParenthesisToken, CloseParenthesisToken, is_operand, is_operator, PlusOperatorToken, ProductOperatorToken, \
    DivisionOperatorToken, is_function, is_trigonometric, LnFunctionToken, LogFunctionToken, \
    is_constant

logger = logging.getLogger(__name__)


class Expression:
    pass


class Equation:
    pass


class EquationNode:
    def __init__(self, coefficient=None, constant=None):
        self.coefficient = coefficient
        self.constant = constant

    def has_constant(self):
        return self.constant is not None

    def has_coef(self):
        return self.coefficient is not None

    def __str__(self):
        return "EquationNode, coeff = {}, constant = {}".format(self.coefficient, self.constant)

    def __repr__(self):
        return self.__str__()


class Parser:
    def parse(self, input):
        logger.debug("Parsing input '%s'", input)

        token_list = tokenize(input)

        logger.debug("Tokens:")
        for tok in token_list:
            logger.debug("    %r", tok)

        # Decide whether it's an expression or an equation
        is_equation = False

        # For equations, convert the equal sign into a "minus" sign and surround the RHS of the equation in parenthesis
        for i, tok in enumerate(token_list):
            if isinstance(tok, EqualSignToken):
                logger.debug("Detected equation")
                is_equation = True
                token_list.pop(i)
                token_list.insert(i, MinusOperatorToken())
                token_list.insert(i + 1, OpenParenthesisToken())
                token_list.append(CloseParenthesisToken())
                break

        # For expressions work out whether we're dealing with normal or postfix expressions
        # If there are two consecutive operands, then it's a postfix (or an invalid) expression
        # TODO: Improve detection of postfix expressions
        is_postfix = False

        for i in range(len(token_list) - 1):
            if isinstance(token_list[i], OperandToken) and isinstance(token_list[i + 1], OperandToken):
                logger.debug("Detected postfix expression")
                is_postfix = True
                break

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

            if is_operand(tok):
                node = EquationNode(constant=tok.value)

            elif is_variable(tok):
                node = EquationNode(coefficient=1)

            elif is_constant(tok):
                node = EquationNode(constant=tok.value)

            else:
                if is_operator(tok):
                    second_operand = stack.pop()
                    first_operand = stack.pop()

                    if isinstance(tok, PlusOperatorToken):
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

                    elif isinstance(tok, MinusOperatorToken):
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

                    elif isinstance(tok, ProductOperatorToken):
                        constant = 0
                        coefficient = None

                        if first_operand.has_constant():
                            if second_operand.has_constant():
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

                        #
                        # if first_operand.has_constant() and second_operand.has_constant():
                        #     constant = first_operand.constant * second_operand.constant
                        #
                        # elif first_operand.has_constant() and second_operand.has_coef():
                        #     coefficient = first_operand.constant * second_operand.coefficient
                        #
                        # elif first_operand.has_coef() and second_operand.has_constant():
                        #     coefficient = first_operand.coefficient * second_operand.constant
                        #
                        # else:
                        #     raise RuntimeError("Unsupported expression, can't have exponential variables")

                        node = EquationNode(coefficient=coefficient, constant=constant)

                    elif isinstance(tok, DivisionOperatorToken):
                        constant = 0
                        coefficient = None

                        if first_operand.has_constant():
                            if second_operand.has_constant():
                                constant += first_operand.constant / second_operand.constant

                            if second_operand.has_coef():
                                if coefficient is None: coefficient = 0
                                coefficient += first_operand.constant / second_operand.coefficient

                        if first_operand.has_coef():
                            if second_operand.has_constant():
                                if coefficient is None: coefficient = 0
                                coefficient += first_operand.coefficient / second_operand.constant

                            if second_operand.has_coef():
                                raise RuntimeError("Unsupported expression, can't have exponential variables")

                        # if first_operand.has_constant() and second_operand.has_constant():
                        #     constant = first_operand.constant / second_operand.constant
                        #
                        # elif first_operand.has_constant() and second_operand.has_coef():
                        #     coefficient = first_operand.constant / second_operand.coefficient
                        #
                        # elif first_operand.has_coef() and second_operand.has_constant():
                        #     coefficient = first_operand.coefficient / second_operand.constant
                        #
                        # else:
                        #     raise RuntimeError("Unsupported expression, can't have exponential variables")

                        node = EquationNode(coefficient=coefficient, constant=constant)

                elif is_function(tok):
                    operand = stack.pop()

                    # Functions are only allowed in simple expressions, not in equations, so there should be no coeffs.
                    if operand.has_coef():
                        raise RuntimeError("Function not allowed in equations")

                    # Make sure there's a value to work with
                    if not operand.has_constant():
                        raise RuntimeError("Missing value for trigonometric function")

                    if is_trigonometric(tok):
                        node = EquationNode(constant=tok.oper(operand.constant))

                    elif isinstance(tok, LnFunctionToken):
                        node = EquationNode(constant=math.log(operand.constant, math.e))

                    elif isinstance(tok, LogFunctionToken):
                        base = 10

                        if tok.has_custom_base:
                            base = stack.pop().constant

                        node = EquationNode(constant=math.log(operand.constant, base))

            if node is not None:
                logger.debug(node)
                stack.append(node)

        logger.debug(stack)

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
