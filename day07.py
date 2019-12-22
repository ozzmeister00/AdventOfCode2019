"""
07
"""

from egc.computer import ElfGuidanceComputer
from utils.solver import ProblemSolver


class Day07ElfGuidanceComputer(ElfGuidanceComputer):
    def __init__(self, *args, **kwargs):
        super(Day07ElfGuidanceComputer, self).__init__(*args, **kwargs)
        self.inputCounter = -1
        self.phase = -1
        self.input = 0

    def GetInput(self):
        """
        Get the current phase setting, a value between 0 and 4

        :return: The phase setting of this computer, if valid
        """
        self.inputCounter += 1

        # if it's the first input call, grab the phase setting
        if self.inputCounter == 0:
            if 0 <= self.phase <= 4:
                return self.phase
            else:
                raise ValueError("Invalid phase setting {}".format(self.phase))
        elif self.inputCounter == 1:
            return self.input
        else:
            raise IndexError("Number of input instructions called exceeds number of available inputs")


class DaySolver07(ProblemSolver):
    def __init__(self):
        super(DaySolver07, self).__init__(7)

        self.testDataPartOne = {('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', '43210'): 43210,
                                ('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0', '01234'): 54321,
                                ('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0','10432'): 65210}
        self.testDataPartTwo = {}

        self.amplifierIDs = ['a', 'b', 'c', 'd', 'e']
        self.phases = [0, 1, 2, 3, 4]

    def ProcessInput(self, data=None):
        """
        :param str data: comma-separated integers

        :returns list[int]: the intcode buffer
        """
        if not data:
            data = self.rawData

        processed = [int(i) for i in data.split(',')]

        return processed

    def _initializeAmplifiers(self, data):
        """

        :return dict: the initialized amplifier computers mapped to str ids
        """
        return {amp: Day07ElfGuidanceComputer(data) for amp in self.amplifierIDs}

    def TestAlgorithm(self, algorithm, part=1):
        """
        Override the algorithm testing method so we can customize
        how we handle input data for testing part 1

        :param func algorithm: the algorithm to test
        :param int part: the part of the day we're testing

        :return bool: if we succeeded
        """
        if part == 2:
            return super(DaySolver07, self).TestAlgorithm(algorithm, part=part)

        for test, expectedResult in self.testDataPartOne.items():
            data, phaseOrder = test

            processed = self.ProcessInput(data=data)
            phaseOrder = [int(i) for i in phaseOrder]

            amplifiers = self._initializeAmplifiers(processed)

            result = self.testPhaseOrder(amplifiers, phaseOrder)

            if result != expectedResult:
                raise Exception("Test on data {} returned result {}".format(test, result))

        return True

    def testPhaseOrder(self, amplifiers, phaseOrder):
        """
        Test the given amplifier buffer based on the input phaseOrder values

        :param dict amplifiers:
        :param list phaseOrder:

        :return int: the output buffer of amplifier e
        """
        amplifiers = amplifiers.copy()

        for i, value in enumerate(self.amplifierIDs):
            amplifiers[value].phase = phaseOrder[i]

        for i, value in enumerate(self.amplifierIDs):
            amplifiers[value].Run()

            if i + 1 < len(self.amplifierIDs):
                amplifiers[self.amplifierIDs[i + 1]].input = amplifiers[value].output

        return amplifiers['e'].output

    def SolvePartOne(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        if not data:
            data = self.processed

        amplifiers = self._initializeAmplifiers(data)

        return amplifiers['e'].output

    def SolvePartTwo(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        if not data:
            data = self.processed


def Main():
    solver = DaySolver07()
    solver.Run()


if __name__ == '__main__':
    Main()
