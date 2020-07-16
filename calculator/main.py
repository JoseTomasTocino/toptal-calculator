import logging

from calculator.parser.parser import Parser


def main():
    p = Parser()

    # p.parse("( A + B ) * ( C + D )")
    # p.parse("3+sin(6*3)-7")
    p.parse("2x + 1 = 2(1-x)")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
