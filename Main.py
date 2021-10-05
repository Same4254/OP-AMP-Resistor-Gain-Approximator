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

'''
    Recursively traverses all of the resistor possibilities for each resistor
    
    We don't know that order does not matter: expression(Ra = 1000, Rb = 1500) == expression(Ra = 1500, Rb = 1000), is not guaranteed
    Thus, just go over all permutations. It's not super efficient, but it's simple and guaranteed to generate the correct result
'''
def approximateHelper(expression : str, targetGain : float, variableNames : [str], localDictionary : {}, index : int):
    if index == 0:
        # All but the last resistor have been chosen. Iterate through all of the last choices and pick the best permutation

        bestGain = 0
        bestResistors = None

        for resistor in resistors:
            # set the parameter to the resistor value
            localDictionary[variableNames[index]] = resistor

            # execute the expression with the values in the localDictionary
            exec("gain = " + expression, globals(), localDictionary)

            # take the better set of resistors
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

'''
    Given the resistor expression and the target gain, return the resistors for the best approximate gain for the target gain
        Using only the standard resistor values
    
    expression -> String representing the equation
    targetGain -> gain to approximate
    
    returns a dictionary where each of the parameters is mapped to the resistor value and "gain" is the best approximation to the target gain 
'''
def approximate(expression : str, targetGain : float):
    # Compile the code to get the list of variable names to put in the local dictionary later
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
        expression = input("Enter a resistor expression you lazy bum: ")

        if expression == "exit":
            break

        targetGain = input("Enter the gain I guess :/ : ")

        if targetGain == "exit":
            break

        print(approximate(expression, float(targetGain)))
        print("-----------------------")
        print()