import math
from multiprocessing import Pool

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

def findClosest(list, value):
    closestValue = list[0]
    for v in list:
        if abs(v - value) < abs(closestValue - value):
            closestValue = v

    return closestValue

def findBest(r10):
    largestError = 10000000000

    # for r2 in resistors:
    #     for r1 in resistors:
    #         for r10 in resistors:
    #             for r11 in resistors:
    #                 for r3 in resistors:
    #                     for p1 in potentiometers:
    #                         for p2 in potentiometers:
    #                             for c1 in capacitors:
    #                                 qFactor = (0.5 * math.sqrt(r2 / r1))
    #                                 frequency = 1 / (2 * math.pi * (c1) * math.sqrt(r1 * r2))
    #                                 # minGain = (r2 * (r10 + r21)) / (2 * r1 * (r11 + p12))
    #                                 # maxGain = (r2 * (r10 + r21)) / (2 * r1 * (r11))
    #
    #                                 minGain = (r2 / (2 * r1)) * (r10 / r11) * (1)
    #                                 maxGain = (r2 / (2 * r1)) * (r10 / r11) * (1 + ((p1 + p2) / r3))
    #
    #                                 qFactorError = abs((qFactor - 0.7) / 0.7)
    #                                 frequencyError = abs((frequency - 200) / 200)
    #                                 minGainError = abs((minGain - 0.4) / 0.4)
    #                                 maxGainError = abs((maxGain - 8) / 8)
    #
    #                                 maxError = max(qFactorError, frequencyError, minGainError, maxGainError)
    #                                 current = {"r1":r1, "r2":r2, "c1":c1,"r10":r10,"r11":r11,"r3":r3,"p1":p1,"p2":p2,"frequency":frequency,"qfactor":qFactor,"minGain":minGain,"maxGain":maxGain,"maxError":maxError}
    #
    #                                 if maxError < largestError:
    #                                     largestError = maxError
    #                                     best = current

    for r10 in resistors:
        for r11 in resistors:
            for r12 in resistors:
                for r13 in resistors:
                    minGain1 = (r10 / r11)
                    maxGain1 = ((r10 * 21) / r11)

                    minGain2 = (r10 / r12)
                    maxGain2 = ((r10 * 21) / r12)

                    minGain3 = (r10 / r13)
                    maxGain3 = ((r10 * 21) / r13)

                    minGain1Error = abs((minGain1 - 0.4) / 0.4)
                    maxGain1Error = abs((maxGain1 - 8) / 8)

                    minGain2Error = abs((minGain2 - 0.2) / 0.2)
                    maxGain2Error = abs((maxGain2 - 4) / 4)

                    minGain3Error = abs((minGain3 - 0.1) / 0.1)
                    maxGain3Error = abs((maxGain3 - 2) / 2)

                    maxError = max(minGain1Error, maxGain1Error, minGain2Error, maxGain2Error,minGain3Error,maxGain3Error)
                    current = {"r10": r10, "r11": r11, "r12":r12,"r13":r13,"minGain": minGain1, "maxGain": maxGain1,"minGain2": minGain2, "maxGain2": maxGain2,"minGain3": minGain3, "maxGain3": maxGain3, "maxError": maxError}

                    if maxError < largestError:
                        largestError = maxError
                        best = current
    return best

if __name__ == '__main__':
    with Pool(4) as p:
        results = p.map(findBest, resistors)
        best = results[0]
        for r in results:
            if r["maxError"] < best["maxError"]:
                best = r

        print(best)