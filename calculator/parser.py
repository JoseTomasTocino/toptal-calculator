import logging

from calculator import tokens
from calculator.tokens import is_variable, is_operand, is_function, is_operator, is_left_paren, is_right_paren, \
    is_constant

logger = logging.getLogger(__name__)


def tokenize(input: str):
    input = input.lower()

    token_list = []

    i = 0
    while i < len(input):
        char = input[i]

        if char == '(':
            token_list.append(tokens.OpenParenthesisToken())

        elif char == ')':
            token_list.append(tokens.CloseParenthesisToken())

        elif char == '+':
            token_list.append(tokens.PlusOperatorToken())

        elif char == '-':
            token_list.append(tokens.MinusOperatorToken())

        elif char == '*':
            token_list.append(tokens.ProductOperatorToken())

        elif char == '/':
            token_list.append(tokens.DivisionOperatorToken())

        elif char == '=':
            token_list.append(tokens.EqualSignToken())

        elif char.isalpha():

            token_strings = {
                'sin': tokens.SinFunctionToken,
                'cos': tokens.CosFunctionToken,
                'tan': tokens.TanFunctionToken,
                'ctan': tokens.CtanFunctionToken,
                'pi': tokens.PiConstantToken,
                'e': tokens.EulerConstantToken,
                'log': tokens.LogFunctionToken,
                'ln': tokens.LnFunctionToken
            }

            for key in token_strings:
                if input[i:i + len(key)] == key:
                    token_list.append(token_strings[key]())
                    i += len(key) - 1
                    break

            # The character was not part of any special token
            else:
                token_components = [char]

                j = i + 1
                while j < len(input) and input[j].isalpha():
                    token_components.append(input[j])
                    j += 1

                i = j - 1
                token_list.append(tokens.VariableToken(''.join(token_components)))

        elif char.isdecimal():
            token_components = [char]

            # Keep consuming decimal characters
            j = i + 1
            while j < len(input) and (input[j].isdecimal() or input[j] == '.'):
                token_components.append(input[j])
                j += 1

            i = j - 1
            token_list.append(tokens.OperandToken(float(''.join(token_components))))

        i += 1

    # Token List postprocessing, in particular:
    # - Add product operator between operand and variable
    # - Add product operator between operand and constant
    # - Add product operator between operand and open parenthesis (except for the Log function)
    # - Add product operator between variable and open parenthesis
    # - Mark LogFunctionToken to have a custom base if followed by two ConstantTokens

    processed_token_list = []

    for i, tok in enumerate(token_list):
        processed_token_list.append(tok)

        if i == len(token_list) - 1:
            break

        if is_operand(tok):

            # - Add product operator between operand and variable
            if is_variable(token_list[i + 1]):
                logger.debug("Adding implicit product operator between operand and variable")
                processed_token_list.append(tokens.ProductOperatorToken())

            elif is_constant(token_list[i + 1]):
                logger.debug("Adding implicit product operator between operand and constant")
                processed_token_list.append(tokens.ProductOperatorToken())

            # - Add product operator between operand and open parenthesis (except for the Log function)
            elif is_left_paren(token_list[i + 1]) and not isinstance(token_list[i - 1], tokens.LogFunctionToken):
                logger.debug("Adding implicit product operator between operand and open parenthesis")
                processed_token_list.append(tokens.ProductOperatorToken())

        elif is_variable(tok):

            # - Add product operator between variable and open parenthesis
            if is_left_paren(token_list[i + 1]):
                logger.debug("Adding implicit product operator between variable and open parenthesis")
                processed_token_list.append(tokens.ProductOperatorToken())

        # - Mark LogFunctionToken to have a custom base if followed by two ConstantTokens or a ConstantToken and open parenthesis
        elif isinstance(tok, tokens.LogFunctionToken) and i < len(token_list) - 2 and is_operand(
                token_list[i + 1]) and (is_constant(token_list[i + 2]) or is_left_paren(token_list[i + 2])):
            tok.has_custom_base = True

    return processed_token_list


def infix_to_postfix(token_list: list):
    precedences = {}
    precedences[tokens.SinFunctionToken] = 4
    precedences[tokens.CosFunctionToken] = 4
    precedences[tokens.TanFunctionToken] = 4
    precedences[tokens.CtanFunctionToken] = 4

    precedences[tokens.LogFunctionToken] = 4
    precedences[tokens.LnFunctionToken] = 4

    precedences[tokens.ProductOperatorToken] = 3
    precedences[tokens.DivisionOperatorToken] = 3
    precedences[tokens.PlusOperatorToken] = 2
    precedences[tokens.MinusOperatorToken] = 2
    precedences[tokens.OpenParenthesisToken] = 1

    op_stack = []
    postfix_token_list = []

    # Shunting-yard algorithm from https://en.wikipedia.org/wiki/Shunting-yard_algorithm#The_algorithm_in_detail
    for token in token_list:
        if is_operand(token) or is_variable(token) or is_constant(token):
            postfix_token_list.append(token)

        elif is_function(token):
            op_stack.append(token)

        elif is_operator(token):
            while op_stack and precedences[type(op_stack[-1])] >= precedences[type(token)] and not is_left_paren(
                    op_stack[-1]):
                postfix_token_list.append(op_stack.pop())

            op_stack.append(token)

        elif is_left_paren(token):
            op_stack.append(token)

        elif is_right_paren(token):
            try:
                while not is_left_paren(op_stack[-1]):
                    postfix_token_list.append(op_stack.pop())

            except IndexError:
                raise RuntimeError("Mismatched parentheses")

            op_stack.pop()

    while op_stack:
        if is_left_paren(op_stack[-1]) or is_right_paren(op_stack[-1]):
            raise RuntimeError("Mismatched parentheses")

        postfix_token_list.append(op_stack.pop())

    return postfix_token_list
