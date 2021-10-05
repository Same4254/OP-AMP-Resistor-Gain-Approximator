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

def approximateHelper(expression, targetGain, variableNames, localDictionary, index):
    if index == 0:
        bestGain = 0
        bestResistors = None

        for resistor in resistors:
            localDictionary[variableNames[index]] = resistor

            exec("gain = " + expression, globals(), localDictionary)

            if bestResistors is None or abs(localDictionary["gain"] - targetGain) < abs(bestGain - targetGain):
                bestGain = localDictionary["gain"]
                bestResistors = localDictionary.copy()

        return bestResistors

    bestResistors = None

    for resistor in resistors:
        localDictionary[variableNames[index]] = resistor
        retValue = approximateHelper(expression, targetGain, variableNames, localDictionary.copy(), index - 1)

        if bestResistors is None or abs(retValue["gain"] - targetGain) < abs(bestResistors["gain"] - targetGain):
            bestResistors = retValue

    return bestResistors


def approximate(expression, targetGain):
    code = parser.expr(expression).compile()
    variableNames = code.co_names

    localDictionary = {}

    return approximateHelper(expression, targetGain, variableNames, localDictionary, len(variableNames) - 1)

##### Manual #####

def expression1(ra: int, rb: int, rc: int, rd: int):
    return (rb / ra) * (rd / rc)

def approximateManual(targetGain):
    bestGain = 0
    bestResistors = []

    for ra in resistors:
        for rb in resistors:
            for rc in resistors:
                for rd in resistors:
                    if(abs(expression1(ra, rb, rc, rd) - targetGain) < abs(bestGain - targetGain)):
                        bestGain = expression1(ra, rb, rc, rd)
                        bestResistors = [ra, rb, rc, rd]

    return (bestGain, bestResistors)

if __name__ == '__main__':
    print(approximate("(Rb / Ra) * (Rd / Rc)", 57))