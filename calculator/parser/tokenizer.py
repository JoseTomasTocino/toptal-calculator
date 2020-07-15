from calculator.parser import tokens


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

    return token_list
