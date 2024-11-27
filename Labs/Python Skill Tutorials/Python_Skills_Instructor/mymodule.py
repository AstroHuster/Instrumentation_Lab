"""
Example of a python module. Contains a variable called answer,
and a function called game.

The triple quotes are python's way of creating a multiple line string.
The convention for modules is that the should have a multiple line string
at the beginning of the module file that contains information on the
module.

19a - Converted to python 3
24a - Convert formatting to f-strings
"""

import random as r

answer = r.randint(1,10)

def game():
    global answer
    done = False
    nGuesses = 0
    while not done:
        guess = int(input("Enter a guess from 1 to 10: "))
        nGuesses += 1
        if guess > answer:
            print("Your guess is too big")
        elif guess == answer:
            print("Correct!")
            done = True
        else:
            print("Your guess is too small")

        if done == True:
            print("Game over, it took you ", nGuesses, " guesses to get the right answer")
            # generate a new answer
            answer = r.randint(1,10)
    return
