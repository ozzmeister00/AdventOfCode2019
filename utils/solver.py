"""
Stores out problem-solver class
"""

import os

from . import constants


class ProblemSolver(object):
    """
    Common class for loading and processing data from each day's challenge
    """
    def __init__(self, day):
        """
        Finds the input data file for this day, and loads the raw contents of that file into
        the rawData property of the instance

        :param int day: the number day for this data
        """
        self.day = day
        self.fileName = 'day{}.txt'.format(str(day).zfill(2))
        self.filePath = os.path.join(constants.getInputsFolder(), self.fileName)

        self.rawData = ''
        # load in the file's data
        if os.path.exists(self.filePath):
            with open(self.filePath, 'r') as fh:
                self.rawData = fh.read()
        else:
            # TODO: Add a warning here
            print("Warning!")

        # leave this open for later access by process input
        self.processed = None
        self.partOneResult = None
        self.partTwoResult = None

        self.testDataPartOne = {}
        self.testDataPartTwo = {}

    def ProcessInput(self, data=None):
        """
        To be implemented by each day's class to process data into a helpful format
        for later handling

        :returns: Processed Input
        """
        raise NotImplementedError()

    def TestAlgorithm(self, algorithm, part=1):
        """
        :param func algorithm: The algorithm function to test on the test data
        :param int part: the part of the day's solution to test

        :returns bool: If the tests passed, otherwise raises exception since we should pass our tests
        """
        testData = self.testDataPartOne
        if part == 2:
            testData = self.testDataPartTwo

        for test in testData:
            processed = self.ProcessInput(data=test)
            result = algorithm(data=processed)
            if result != testData[test]:
                raise Exception("Test on data {} returned result {}".format(processed, result))

        return True

    def SolvePartOne(self, data=None):
        """
        Method to be implemented to solve for part one

        :param object data: optional data to process

        :returns: The solution for part one
        """
        raise NotImplementedError()

    def SolvePartTwo(self, data=None):
        """
        Method to be implemented to solve for part two

        :param object data: optional data to operate on

        :returns: The solution for part two
        """
        raise NotImplementedError()

    def Run(self):
        """
        Run the full suite of testing and processing for this day
        """
        self.processed = self.ProcessInput()
        try:
            print('TestResult:', self.TestAlgorithm(self.SolvePartOne))
            print('Result: ', self.SolvePartOne())
            print('TestResult2:', self.TestAlgorithm(self.SolvePartTwo, part=2))
            print('Result: ', self.SolvePartTwo())
        except NotImplementedError:
            print("Testing not complete due to some parts not being implemented properly")
