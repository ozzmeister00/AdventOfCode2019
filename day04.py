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

    def Run(self):
        self.ProcessInput()

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


def IsValidPassword(value):
    """
    A password is valid if:
        It is a six-digit number.
        The value is within the range given in your puzzle input.
        Two adjacent digits are the same (like 22 in 122345).
        Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

    :param int value:
    :return bool: if the input password is, in fact, valid
    """
    stringValue = str(value)
    listValue = [int(i) for i in stringValue]

    if not(99999 < value < 1000000):
        return False

    foundADouble = False
    for index, value in enumerate(stringValue):
        if index + 1 < len(stringValue):
            if value == stringValue[index + 1]:
                foundADouble = True
                break

    if not foundADouble:
        return False

    for index, value in enumerate(listValue):
        if index + 1 < len(listValue):
            if listValue[index + 1] < value:
                return False

    return True


def IsReallyValidPassword(value):
    """
      A password is valid if:
          It is a six-digit number.
          The value is within the range given in your puzzle input.
          Two adjacent digits are the same (like 22 in 122345).
          Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

      :param int value:
      :return bool: if the input password is, in fact, valid
      """
    stringValue = str(value)
    listValue = [int(i) for i in stringValue]

    if not (99999 < value < 1000000):
        return False

    # check if the string even has doubles by uniquing the list of ints and seeing if that condenses our number at all
    # this gives us a nice early out
    if len(list(set(listValue))) == 6:
        return False

    pointer = 0
    matchingCounter = 0
    hasDouble = False
    while pointer < 5:
        # if the next digit matches us
        if listValue[pointer] == listValue[pointer + 1]:
            matchingCounter += 1
        # if the next value no longer matches our current value
        else:
            # if we ended our streak with 2, then we found a double
            if matchingCounter == 1:
                hasDouble = True
                break

            # reset the matching counter
            matchingCounter = 0

        # move to the next thing to test
        pointer += 1

    # double check if we got to the end of the string and didn't already report a double
    if matchingCounter == 1:
        hasDouble = True

    if not hasDouble:
        return False

    for index, value in enumerate(listValue):
        if index + 1 < len(listValue):
            if listValue[index + 1] < value:
                return False

    return True


def PartOne():
    """
    Prints the length of the list of valid passwords in the range determined by my puzzle input
    """
    passwords = [password for password in range(231832, 767346+1) if IsValidPassword(password)]
    print(len(passwords))


def PartTwo():
    """
    Prints the length of the list of valid passwords in the range determined by my puzzle input
    """
    passwords = [password for password in range(231832, 767346) if IsReallyValidPassword(password)]
    print(len(passwords))


def Main():
    PartOne()
    PartTwo()


if __name__ == '__main__':
    Main()
