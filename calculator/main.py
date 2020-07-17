import logging

from calculator.parser.parser import Parser


def main():
    p = Parser()

    # p.parse("( A + B ) * ( C + D )")
    # p.parse("3+sin(6*3)-7")
    # p.parse("2x + 1 = 2(1-x)")
    # p.parse("2x + 1 = 2 - 2x")
    # p.parse("(3+(4-1))*5")
    # p.parse("2 * x + 0.5 = 1")
    # p.parse("2x + 1 = 2(1-x)")
    p.parse("5(2+3x)")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(level=logging.INFO)
    main()
