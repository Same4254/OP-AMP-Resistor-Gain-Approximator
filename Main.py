import parser

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

potentiometers = [
    5000,
    10000
]

'''
    Recursively traverses all of the resistor possibilities for each resistor
    
    We don't know that order does not matter: expression(Ra = 1000, Rb = 1500) == expression(Ra = 1500, Rb = 1000), is not guaranteed
    Thus, just go over all permutations. It's not super efficient, but it's simple and guaranteed to generate the correct result
'''
def approximateHelper(expressions : [str], targetGains : [float], variableNames : [str], potentiometerNames : [str], localDictionary : {}, index : int):
    if index == 0:
        # All but the last resistor have been chosen. Iterate through all of the last choices and pick the best permutation

        bestGainDifference = 0
        bestResistors = None

        possibleValues = potentiometers if variableNames[index] in potentiometerNames else resistors

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

        return bestResistors

    bestResistors = None

    possibleValues = potentiometers if variableNames[index] in potentiometerNames else resistors

    for resistor in possibleValues:
        localDictionary[variableNames[index]] = resistor
        retValue = approximateHelper(expressions, targetGains, variableNames, potentiometerNames, localDictionary.copy(), index - 1)

        if bestResistors is None or retValue["gain"] < bestResistors["gain"]:
            bestResistors = retValue

    return bestResistors

'''
    Given the resistor expression and the target gain, return the resistors for the best approximate gain for the target gain
        Using only the standard resistor values
    
    expression -> String representing the equation
    targetGain -> gain to approximate
    
    returns a dictionary where each of the parameters is mapped to the resistor value and "gain" is the best approximation to the target gain 
'''
def approximate(expressions : [str], potentiometers : [str], targetGains : [float]):
    # Compile the code to get the list of variable names to put in the local dictionary later
    variableNames = []

    for expression in expressions:
        code = parser.expr(expression).compile()
        for name in code.co_names:
            if name not in variableNames:
                variableNames.append(name)

    localDictionary = {}

    bestResistors = approximateHelper([compile(source="gain = " + expression, filename="expression", mode="exec") for expression in expressions], targetGains, variableNames, potentiometers, localDictionary, len(variableNames) - 1)

    del bestResistors["gain"]

    for i in range(len(expressions)):
        exec("gain" + str(i + 1) + " = " + expressions[i], globals(), bestResistors)

    return bestResistors

'''
    Recursively traverses all of the resistor possibilities for each resistor

    We don't know that order does not matter: expression(Ra = 1000, Rb = 1500) == expression(Ra = 1500, Rb = 1000), is not guaranteed
    Thus, just go over all permutations. It's not super efficient, but it's simple and guaranteed to generate the correct result
'''
def approximateHelperFAST(expressions: [str], targetGains: [float], variableNames: [str], potentiometerNames: [str],
                      localDictionary: {}, index: int):
    if index == 0:
        # All but the last resistor have been chosen. Iterate through all of the last choices and pick the best permutation

        bestGainDifference = 0
        bestResistors = None

        possibleValues = potentiometers if variableNames[index] in potentiometerNames else resistors

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

    possibleValues = potentiometers if variableNames[index] in potentiometerNames else resistors

    for resistor in possibleValues:
        localDictionary[variableNames[index]] = resistor
        retValue = approximateHelperFAST(expressions, targetGains, variableNames, potentiometerNames, localDictionary.copy(),
                                     index - 1)

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


def approximateFAST(expressions: [str], potNames: [str], targetGains: [float]):
    # Compile the code to get the list of variable names to put in the local dictionary later
    variableNames = []

    for expression in expressions:
        code = parser.expr(expression).compile()
        for name in code.co_names:
            if name not in variableNames:
                variableNames.append(name)

    localDictionary = {}

    bestResistors = approximateHelperFAST(
        [compile(source="gain = " + expression, filename="expression", mode="exec", optimize=2) for expression in expressions],
        targetGains, variableNames, potNames, localDictionary, len(variableNames) - 1)

    del bestResistors["gain"]

    for i in range(len(expressions)):
        exec("gain" + str(i + 1) + " = " + expressions[i], globals(), bestResistors)

    return bestResistors

if __name__ == '__main__':
    print("Welcome to the OP Amp Resistor Gain Approxilator!!")
    print("Made by Sam S.")
    print("-----------------------")
    print()

    print("-----------------------")
    print()

    print("Type exit to leave the program")

    print("-----------------------")
    print()

    print("Expressions follow python syntax. Variable names do not matter")
    print("Example expression: (Rb / Ra) * (Rd / Rc)")
    print("-----------------------")
    print()

    while True:
        numExpressions = int(input("How many expressions will there be? "))

        if numExpressions == "exit":
            return

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

        numPots = int(input("How many potentiometers are there?: "))
        pots = []
        for i in range(numPots):
            potName = input("Enter the name of a potentiometer: ")
            if potName == "exit":
                break

            pots.append(potName)

        fast = input("Would you like to use the fast approximation? It is faster, but not as accurate.... Sowwy: ")

        if fast == "yes":
            print("Running Fast Algorithm")
            print(approximateFAST(expressions, pots, targetGains))
        else:
            print("Running Exact Algorithm")
            print(approximate(expressions, pots, targetGains))

        print("-----------------------")
        print()