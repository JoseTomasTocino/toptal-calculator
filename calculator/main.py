import logging

from calculator import evaluator


def main():
    expression = None
    notation = None

    while expression is None or expression.strip() == '':
        expression = input("Please enter the expression: ")

    while notation not in ['y', 'n']:
        notation = input("Use postfix notation? [y/n]: ")

    print("Output:", evaluator.evaluate(expression))


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    main()
