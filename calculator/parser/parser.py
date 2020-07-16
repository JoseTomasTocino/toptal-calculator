import logging

from calculator.parser.tokenizer import tokenize, infix_to_postfix
from calculator.parser.tokens import EqualSignToken, OperandToken, is_variable

logger = logging.getLogger(__name__)


class Expression:
    pass


class Equation:
    pass


class Parser:
    def parse(self, input):
        logger.debug("Parsing input '%s'", input)

        token_list = tokenize(input)

        logger.debug("Tokens:")
        for tok in token_list:
            logger.debug("    %r", tok)

        # Decide whether it's an expression or an equation
        is_equation = False

        for tok in token_list:
            if isinstance(tok, EqualSignToken):
                is_equation = True
                break

        if is_equation:
            self.process_equation(token_list)
        else:
            self.process_expression(token_list)

    def process_equation(self, token_list):
        logger.debug("Detected equation")

        lhs_tokens = []
        rhs_tokens = []

        for i, tok in enumerate(token_list):
            if isinstance(tok, EqualSignToken):
                lhs_tokens = token_list[:i]
                rhs_tokens = token_list[i + 1:]

        logger.debug("Converting LHS to postfix")
        token_list = infix_to_postfix(lhs_tokens)

        logger.debug("Tokens:")
        for tok in token_list:
            logger.debug("    %r", tok)

        logger.debug("Converting RHS to postfix")
        token_list = infix_to_postfix(rhs_tokens)

        logger.debug("Tokens:")
        for tok in token_list:
            logger.debug("    %r", tok)

    def process_expression(self, token_list, accept_variables=False):
        logger.debug("Detected expression")

        # If there's an expression but there are variables, raise an error
        if not accept_variables:
            for tok in token_list:
                if is_variable(tok):
                    raise RuntimeError("Found variable outside equation")

        # For expressions work out whether we're dealing with normal or postfix expressions
        # If there are two consecutive operands, then it's a postfix (or an invalid) expression
        # TODO: Improve detection of postfix expressions
        is_postfix = False

        for i in range(len(token_list) - 1):
            if isinstance(token_list[i], OperandToken) and isinstance(token_list[i + 1], OperandToken):
                is_postfix = True
                break

        # Convert to postfix if needed
        if not is_postfix:
            logger.debug("Converting to postfix")
            token_list = infix_to_postfix(token_list)

            logger.debug("Tokens:")
            for tok in token_list:
                logger.debug("    %r", tok)
