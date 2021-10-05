# OP-AMP-Resistor-Gain-Approximator
Python program that will approximate the gain of an op amp with the given resistor expression and a list of possible resistors to choose from

## Why
In electrical engineering when designing an operational amplifier circuit, there will come a time when you have a desired gain to be caused by the op amp. The gain is a function of the resistor values. Thus given a gain, one must choose a set of standard resistor values that best approximate the desired gain. This program automates this proocess

## Goal
The end goal was to have a function that would accept an expression for the resistors and the gain they must create. This function would then choose the best set of standard resistor values that best approximated this desired gain
```py
>> approximate(expression = "(Rb / Ra) * (Rd / Rc)", gain = 57)
{'Rc': 1100, 'Rd': 200000, 'Ra': 5100, 'Rb': 1600, 'gain': 57.040998217468804}
```

## How to use
If your computer has python 3, it should be able to run this. Simply download the code and run the main.py file. This will open a terminal and prompt you with instructions
