"""
--- Day 4: Secure Container ---
You arrive at the Venus fuel depot only to discover it's protected by a password.
The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle input is 231832-767346.
"""

from utils.solver import ProblemSolver


class DaySolver04(ProblemSolver):
    def __init__(self):
        super(DaySolver04, self).__init__(4)

        self.testDataPartOne = {}
        self.testDataPartTwo = {}

    def ProcessInput(self, data=None):
        """
        :param str data:
        """
        if not data:
            data = self.rawData

        processed = []

        # process your data here

        return processed

    def SolvePartOne(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        if not data:
            data = self.processed

    def SolvePartTwo(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        if not data:
            data = self.processed


def Main():
    solver = DaySolver04()
    solver.Run()


if __name__ == '__main__':
    Main()        