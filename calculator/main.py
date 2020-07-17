import logging

from calculator.parser.parser import Parser


# input: (3+(4-1))*5
# output: 30
#
# input: 2 * x + 0.5 = 1
# output: x = 0.25
#
# input: 2x + 1 = 2(1-x)
# output: x = 0.25
#
# input: Log(10)
# output: 1
#
# input: Log10
# output: 1
#
# input: Log100(10)
# output: 0.5
#
# input: sin(pi) or sinpi
# output: 0
#
# input: sin(1.5pi) or sin(1.5*pi)
# output: -1

def main():
    p = Parser()

    # p.parse("( A + B ) * ( C + D )")
    # p.parse("3+sin(6*3)-7")
    # p.parse("2x + 1 = 2(1-x)")
    # p.parse("2x + 1 = 2 - 2x")
    # p.parse("(3+(4-1))*5")
    # p.parse("2 * x + 0.5 = 1")
    # p.parse("2x + 1 = 2(1-x)")
    # p.parse("5(2+3x)")
    p.parse("(3+(4-1))*5")
    p.parse("2 * x + 0.5 = 1")
    p.parse("2x + 1 = 2(1-x)")
    p.parse("Log(10)")
    p.parse("Log10")
    p.parse("Log100(10)")
    p.parse("sinpi")
    p.parse("sin(pi)")
    p.parse("sin(1.5pi)")
    p.parse("sin(1.5*pi)")
    # p.parse("sin(1.5pi)")


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    main()
