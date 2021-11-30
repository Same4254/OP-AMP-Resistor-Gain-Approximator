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

    for r2 in resistors:
        # r1 = r2 / 1.96
        # r1 = findClosest(resistors, r1)
        for r1 in resistors:



            for c1 in capacitors:
                for c2 in capacitors:
            # c1 = 1 / (2 * math.pi * 200 * math.sqrt(r1 * r2))
            # c1 = findClosest(capacitors, c1)



                # r11 = findClosest(resistors, (r2 * r10) / (2 * r1 * 8))
                # p12 = findClosest(potentiometers, (((r2 * r10) / (2 * r1)) - (0.4 * r11)) / 0.4)

                    for r11 in resistors:
                        for r21 in resistors:
                            for p12 in potentiometers:
                                qFactor = (0.5 * math.sqrt(r2 / r1))
                                frequency = 1 / (2 * math.pi * (c1 + c2) * math.sqrt(r1 * r2))
                                minGain = (r2 * (r10 + r21)) / (2 * r1 * (r11 + p12))
                                maxGain = (r2 * (r10 + r21)) / (2 * r1 * (r11))

                                qFactorError = abs((qFactor - 0.7) / 0.7)
                                frequencyError = abs((frequency - 200) / 200)
                                minGainError = abs((minGain - 0.4) / 0.4)
                                maxGainError = abs((maxGain - 8) / 8)

                                maxError = max(qFactorError, frequencyError, minGainError, maxGainError)
                                current = {"r1":r1, "r2":r2, "c1":c1,"c2":c2,"r10":r10,"r11":r11,"p12":p12,"r21":r21,"frequency":frequency,"qfactor":qFactor,"minGain":minGain,"maxGain":maxGain,"maxError":maxError}

                                if maxError < largestError:
                                    largestError = maxError
                                    best = current
    return best

if __name__ == '__main__':
    with Pool(8) as p:
        results = p.map(findBest, resistors)
        best = results[0]
        for r in results:
            if r["maxError"] < best["maxError"]:
                best = r

        print(best)