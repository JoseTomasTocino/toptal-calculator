import logging

from calculator import evaluator


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
    # evaluator.evaluate("( A + B ) * ( C + D )")
    # evaluator.evaluate("3+sin(6*3)-7")
    # evaluator.evaluate("2x + 1 = 2(1-x)")
    # evaluator.evaluate("2x + 1 = 2 - 2x")
    # evaluator.evaluate("(3+(4-1))*5")
    # evaluator.evaluate("2 * x + 0.5 = 1")
    # evaluator.evaluate("2x + 1 = 2(1-x)")
    # evaluator.evaluate("(x-2)*(2-3)=0")
    # evaluator.evaluate("4x-7(2-x)=3x+2")
    # evaluator.evaluate("2(w+3)-10=6(32-3w)")

    # evaluator.evaluate("(4-2z)/3 = 3/4 - (5z)/6")

    # evaluator.evaluate("20 / (2x) = 5", False)
    # evaluator.evaluate("(3(7x-1)+10x-4+3x)=90x+1")
    evaluator.evaluate("sin(pi)")

    # evaluator.evaluate("(3+(4-1))*5")
    # evaluator.evaluate("2 * x + 0.5 = 1")
    # evaluator.evaluate("2x + 1 = 2(1-x)")
    # evaluator.evaluate("Log(10)")
    # evaluator.evaluate("Log10")
    # evaluator.evaluate("Log100(10)")
    # evaluator.evaluate("sinpi")
    # evaluator.evaluate("sin(pi)")
    # evaluator.evaluate("sin(1.5pi)")
    # evaluator.evaluate("sin(1.5*pi)")


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    main()
