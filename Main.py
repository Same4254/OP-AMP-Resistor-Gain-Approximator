import parser
import math

# standard resistors

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

rResistors = resistors.copy()
rResistors.reverse()

potentiometers = [
    5000,
    10000
]

rPotentiometers = potentiometers.copy()
rPotentiometers.reverse()

capacitors = [
    100*(10**(-12)),
    220*(10**(-12)),
    330*(10**(-12)),
    470*(10**(-12)),
    1*(10**(-9)),
    1.5*(10**(-9)),
    2.2*(10**(-9)),
    3.3*(10**(-9)),
    4.7*(10**(-9)),
    10*(10**(-9)),
    15*(10**(-9)),
    22*(10**(-9)),
    33*(10**(-9)),
    47*(10**(-9)),
    0.1*(10**(-6)),
    0.15*(10**(-6)),
    0.22*(10**(-6)),
    0.33*(10**(-6)),
    0.47*(10**(-6)),
    0.1*(10**(-6)),
]

rCapacitors = capacitors.copy()
rCapacitors.reverse()


'''
    Recursively traverses all of the resistor possibilities for each resistor

    We don't know that order does not matter: expression(Ra = 1000, Rb = 1500) == expression(Ra = 1500, Rb = 1000), is not guaranteed
    Thus, just go over all permutations. It's not super efficient, but it's simple and guaranteed to generate the correct result
'''
def approximateHelperFAST(expressions: [str], targetGains: [float], variableNames: [str],
                      localDictionary: {}, index: int):
    if index == 0:
        # All but the last resistor have been chosen. Iterate through all of the last choices and pick the best permutation

        bestGainDifference = 0
        bestResistors = None

        # possibleValues = potentiometers if variableNames[index] in potentiometerNames else resistors
        if variableNames[index].lower()[0] == "r":
            possibleValues = resistors

        if variableNames[index].lower()[0] == "p":
            possibleValues = potentiometers

        if variableNames[index].lower()[0] == "c":
            possibleValues = capacitors

        for resistor in possibleValues:
            # set the parameter to the resistor value
            localDictionary[variableNames[index]] = resistor

            gainDifference = 0

            for i in range(len(expressions)):
                exec(expressions[i], globals(), localDictionary)
                gainDifference += abs(localDictionary["gain"] - targetGains[i])

            if bestResistors is None or gainDifference < bestGainDifference:
                bestGainDifference = gainDifference
                bestResistors = localDictionary.copy()
                bestResistors["gain"] = bestGainDifference
            elif gainDifference > bestGainDifference:
                return bestResistors

        return bestResistors

    bestResistors = None

    # possibleValues = potentiometers if variableNames[index] in potentiometerNames else resistors
    if variableNames[index].lower()[0] == "r":
        possibleValues = resistors

    if variableNames[index].lower()[0] == "p":
        possibleValues = potentiometers

    if variableNames[index].lower()[0] == "c":
        possibleValues = capacitors

    for resistor in possibleValues:
        localDictionary[variableNames[index]] = resistor
        retValue = approximateHelperFAST(expressions, targetGains, variableNames, localDictionary.copy(), index - 1)

        if bestResistors is None or retValue["gain"] < bestResistors["gain"]:
            bestResistors = retValue
        elif retValue["gain"] > bestResistors["gain"]:
            return bestResistors

    return bestResistors


'''
    Given the resistor expression and the target gain, return the resistors for the best approximate gain for the target gain
        Using only the standard resistor values

    expression -> String representing the equation
    targetGain -> gain to approximate

    returns a dictionary where each of the parameters is mapped to the resistor value and "gain" is the best approximation to the target gain
'''


def approximateFAST(expressions: [str], targetGains: [float]):
    # Compile the code to get the list of variable names to put in the local dictionary later
    variableNames = []

    for expression in expressions:
        code = parser.expr(expression).compile()
        for name in code.co_names:
            if name not in variableNames and name != "math" and name != "pi" and name != "sqrt":
                variableNames.append(name)

    print(variableNames)

    localDictionary = {}

    bestResistors = approximateHelperFAST(
        [compile(source="gain = " + expression, filename="expression", mode="exec", optimize=2) for expression in expressions],
        targetGains, variableNames, localDictionary, len(variableNames) - 1)

    del bestResistors["gain"]

    for i in range(len(expressions)):
        exec("gain" + str(i + 1) + " = " + expressions[i], globals(), bestResistors)

    return bestResistors

if __name__ == '__main__':
    # expressions = ["1/(2 * math.pi * c1 * math.sqrt(R1 * R2))", "0.5 * math.sqrt(R2 / R1)", "(R2 * R10)/(2 * R1 * (R11 + P12))", "(R2 * R10)/(2 * R1 * (R11))",
    #                "1/(2 * math.pi * c2 * math.sqrt(R4 * R3))", "0.5 * math.sqrt(R3 / R4)", "(R3 * R10)/(2 * R4 * (R13 + P14))", "(R3 * R10)/(2 * R4 * (R13))",
    #                "1/(2 * math.pi * c2 * math.sqrt(R5 * R6))", "0.5 * math.sqrt(R5 / R6)", "(R5 * R10)/(2 * R6 * (R15 + P16))", "(R5 * R10)/(2 * R6 * (R15))"]
    # targetGains = [200, 0.7, 0.4, 8,
    #                1000, 0.7, 0.2, 4,
    #                 5000, 0.7, 0.1, 2]
    #
    # print(approximateFAST(expressions, targetGains))
    #
    # expressions = ["1/(2 * math.pi * (c1 + c2) * math.sqrt(R1 * R2))", "0.5 * math.sqrt(R2 / R1)", "(R2 * R10)/(2 * R1 * (R11 + R20 + P12))", "(R2 * R10)/(2 * R1 * (R11 + R20))"]
    #                # "1/(2 * math.pi * c2 * math.sqrt(R4 * R3))", "0.5 * math.sqrt(R3 / R4)", "(R3 * R10)/(2 * R4 * (R13 + P14))", "(R3 * R10)/(2 * R4 * (R13))"]
    # # "1/(2 * math.pi * c2 * math.sqrt(R5 * R6))", "0.5 * math.sqrt(R5 / R6)", "(R5 * R10)/(2 * R6 * (R15 + P16))", "(R5 * R10)/(2 * R6 * (R15))"]
    # targetGains = [200, 0.7, 0.4, 8]
    #                # 1000, 0.7, 0.2, 4]
    # # 5000, 0.7, 0.1, 2]
    # print(approximateFAST(expressions, targetGains))
    # print(approximateFAST(expressions, targetGains, {"R1": True, "R2": True, "R10": False, "R11" : True, "P12" : True, "R4" : True, "R3" : True, "R13" : True, "P14" : True, "R5" : True, "R6" : True, "R15" : True, "P16" : True, "c1" : True, "c2" : True, "c3" : True}))

    # {'P16': 10000, 'R15': 20000, 'R6': 1000, 'R5': 1000, 'P14': 10000, 'R13': 1000, 'R3': 1100, 'R4': 20000,
    #  'c2': 3.3000000000000004e-08, 'P12': 10000, 'R11': 1000, 'R10': 75000, 'R2': 1100, 'R1': 5100, 'c1': 3.3e-07,
    #  'gain1': 203.62202921536723, 'gain2': 0.232210182006412, 'gain3': 0.7352941176470589, 'gain4': 8.088235294117647,
    #  'gain5': 1028.2408448099543, 'gain6': 0.11726039399558574, 'gain7': 0.1875, 'gain8': 2.0625,
    #  'gain9': 4822.877063390768, 'gain10': 0.5, 'gain11': 1.25, 'gain12': 1.875}

    print("Welcome to the OP Amp Resistor Gain Approxilator!!")
    print("Made by Sam S.")
    print("-----------------------")
    print()

    print("Type exit to leave the program")

    print("-----------------------")
    print()

    print("Expressions follow python syntax. Variable names do not matter")
    print("Example expression: (Rb / Ra) * (Rd / Rc)")
    print("-----------------------")
    print("Resistors begin with r, capacitors: c, potentiometers: p")
    print()

    while True:
        numExpressions = int(input("How many expressions will there be? "))

        if numExpressions == "exit":
            break

        expressions = []
        targetGains = []

        for i in range(numExpressions):
            expression = input("Enter a resistor expression you lazy bum: ")

            if expression == "exit":
                break

            targetGain = input("Enter the target gain I guess :/ : ")

            if targetGain == "exit":
                break

            expressions.append(expression)
            targetGains.append(float(targetGain))

        print(approximateFAST(expressions, targetGains))

        print("-----------------------")
        print()