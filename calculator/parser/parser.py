from calculator.parser.tokenizer import Tokenizer
from calculator.parser.tokens import EqualSignToken, OperandToken


class Expression:
    pass


class Equation:
    pass


class Parser:
    def parse(self, input):
        tk = Tokenizer()
        token_list = tk.tokenize(input)

        # Decide whether it's an expression or an equation
        is_equation = False
        for tok in token_list:
            if isinstance(tok, EqualSignToken):
                is_equation = True
                break

        if is_equation:
            pass

        else:
            # For expressions work out whether we're dealing with normal or postfix expressions
            # If there are two consecutive operands, then it's a postfix (or an invalid) expression
            is_postfix = False
            for i in range(len(token_list) - 1):
                if isinstance(token_list[i], OperandToken) and isinstance(token_list[i + 1], OperandToken):
                    is_postfix = True
                    break

            if is_postfix:
                pass

            else:
                pass
