import parser

resistors = [
    1000,
    1100,
    1300,
    1600,
    2000,
    2200,
    3300,
    5100,
    7500,
    10000,
    15000,
    20000,
    33000,
    51000,
    75000,
    100000,
    200000,
    510000,
    1000000
]

def expression1(ra: int, rb: int, rc: int, rd: int):
    return (rb / ra) * (rd / rc)

def approximate(expression, gain):
    code = parser.expr(expression).compile()
    variableNames = code.co_names

    localDictionary = {}

    bestGain = 0
    bestResistors = []

    for ra in resistors:
        for rb in resistors:
            for rc in resistors:
                for rd in resistors:
                    if(abs(expression1(ra, rb, rc, rd) - gain) < abs(bestGain - gain)):
                        bestGain = expression1(ra, rb, rc, rd)
                        bestResistors = [ra, rb, rc, rd]

    return (bestGain, bestResistors)

if __name__ == '__main__':
    # expression = "(A / B) * (C / D)"

    expression = "A + 1"

    code = parser.expr(expression).compile()

    print(code.co_names)

    ldict = {"A": 4}

    exec("ret = " + expression, globals(), ldict)

    print(ldict["ret"])

    # print(approximate(57))