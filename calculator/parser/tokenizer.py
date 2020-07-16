from calculator.parser import tokens
from calculator.parser.tokens import is_variable, is_operand, is_function, is_operator, is_left_paren, is_right_paren, \
    is_constant


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
    # - Add product operator between operand and open parenthesis

    processed_token_list = []

    for i, tok in enumerate(token_list):
        processed_token_list.append(tok)

        if is_operand(tok) and i < len(token_list) - 1:
            if is_variable(token_list[i + 1]):
                processed_token_list.append(tokens.ProductOperatorToken())

            elif is_left_paren(token_list[i + 1]):
                processed_token_list.append(tokens.ProductOperatorToken())

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

    # for token in token_list:
    #     if isinstance(token, tokens.OperandToken) or isinstance(token, tokens.VariableToken):
    #         postfix_token_list.append(token)
    #
    #     elif isinstance(token, tokens.OpenParenthesisToken):
    #         op_stack.append(token)
    #
    #     elif isinstance(token, tokens.CloseParenthesisToken):
    #         topToken = op_stack.pop()
    #
    #         while not isinstance(topToken, tokens.OpenParenthesisToken):
    #             postfix_token_list.append(topToken)
    #             topToken = op_stack.pop()
    #     else:
    #         while op_stack and (precedences[type(op_stack[-1])] >= precedences[type(token)]):
    #             postfix_token_list.append(op_stack.pop())
    #         op_stack.append(token)
    #
    # while op_stack:
    #     postfix_token_list.append(op_stack.pop())

    return postfix_token_list

    pass
