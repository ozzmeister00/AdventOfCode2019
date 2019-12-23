"""
07
"""
import itertools

from egc.computer import ElfGuidanceComputer
from utils.solver import ProblemSolver


class Day07ElfGuidanceComputer(ElfGuidanceComputer):
    def __init__(self, ampID, *args, **kwargs):
        super(Day07ElfGuidanceComputer, self).__init__(*args, **kwargs)
        self.ampID = ampID
        self.inputCounter = -1
        self.phase = -1
        self.input = 0
        self.output = 0

    def _store(self):
        """
        Stores the result of the computer's GetInput function and stores its value at the position specified

        :returns int: The number of parameters used in the instruction
        """
        value = self.GetInput()
        if value is not False:
            self._setValueForParameter(0, value)

            return 2

        return 0

    def GetInput(self):
        """
        Get the current phase setting, a value between 0 and 4

        :return: The phase setting of this computer, if valid
        """
        self.inputCounter += 1

        # if it's the first input call, grab the phase setting
        if self.inputCounter == 0:
            return self.phase
        else:
            return self.input


class Day07ConcurrentComputer(Day07ElfGuidanceComputer):
    def __init__(self, *args, **kwargs):
        super(Day07ConcurrentComputer, self).__init__(*args, **kwargs)
        self.paused = False
        self.next = -1
        self.input = False
        self.paused = False

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        self._input = value
        self.paused = False

    def step(self):
        super(Day07ConcurrentComputer, self).step()
        #print(self.ampID, self.currentIndex, self.buffer)

    def GetInput(self):
        self.inputCounter += 1
        # if we don't have an input signal, pause
        if self.input is False:
            self.paused = True
            return False

        if self.inputCounter > 0:
            output = self.input
            self.input = False
            return output
        else:
            return self.phase

    def Output(self, value):
        """
        On output, pause execution until we recieve a new input signal

        :param value:
        """
        super(Day07ConcurrentComputer, self).Output(value)

    def RunUntilOutput(self):
        while not self.paused and not self.finished:
            self.step()


class DaySolver07(ProblemSolver):
    def __init__(self):
        super(DaySolver07, self).__init__(7)

        self.testDataPartOne = {('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', '43210'): 43210,
                                ('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0', '01234'): 54321,
                                ('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0','10432'): 65210}
        self.testDataPartTwo = {('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5', '98765'): 139629729,
                                ('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10', '97856'): 18216
                                }

        self.amplifierIDs = ['a', 'b', 'c', 'd', 'e']
        self.nextAmplifier = {'a':'b',
                              'b':'c',
                              'c':'d',
                              'd':'e',
                              'e':'a'}
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

    def _initializeAmplifiers(self, data, amplifierClass=Day07ElfGuidanceComputer):
        """

        :return dict: the initialized amplifier computers mapped to str ids
        """
        return {amp: amplifierClass(amp, data.copy()) for amp in self.amplifierIDs}

    def TestAlgorithm(self, algorithm, part=1):
        """
        Override the algorithm testing method so we can customize
        how we handle input data for testing part 1

        :param func algorithm: the algorithm to test
        :param int part: the part of the day we 're testing

        :return bool: if we succeeded
        """
        if part == 2:
            for test, expectedResult in self.testDataPartTwo.items():
                data, phaseOrder = test

                processed = self.ProcessInput(data=data)
                phaseOrder = [int(i) for i in phaseOrder]

                amplifiers = self._initializeAmplifiers(processed, amplifierClass=Day07ConcurrentComputer)

                result = self.testPhaseOrderConcurrent(amplifiers, phaseOrder)

                if result != expectedResult:
                    raise Exception("Test on Part2 data {} returned result {}".format(test, result))

        else:
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

        amplifiers['a'].input = 0

        for i, value in enumerate(self.amplifierIDs):
            amplifiers[value].Run()

            if i + 1 < len(self.amplifierIDs):
                amplifiers[self.amplifierIDs[i + 1]].input = amplifiers[value].output

        return amplifiers['e'].output

    def testPhaseOrderConcurrent(self, amplifiers, phaseOrder):
        amplifiers = amplifiers.copy()

        # tell the amplifiers who to talk to next
        for amp in amplifiers:
            amplifiers[amp].next = self.nextAmplifier[amp]

        # populate the input buffer with the phase of the amplifier to start
        for i, value in enumerate(self.amplifierIDs):
            amplifiers[value].phase = phaseOrder[i]

        # pre-populate the second input of the 'a' amplifier
        amplifiers['a'].input = 0

        allFinished = False

        while not allFinished:
            for ampID, amplifier in amplifiers.items():
                #print(ampID)
                if not amplifier.finished:
                    amplifier.RunUntilOutput()

                    amplifiers[amplifier.next].input = amplifier.output

            allFinished = all([amplifier.finished for amplifier in amplifiers.values()])

        return amplifiers['e'].output

    def SolvePartOne(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        self.phases = [0, 1, 2, 3, 4]

        if not data:
            data = self.processed

        phaseOrderPermutations = itertools.permutations(self.phases, len(self.phases))

        results = []

        for phaseOrder in phaseOrderPermutations:
            amplifiers = self._initializeAmplifiers(data)
            results.append(self.testPhaseOrder(amplifiers, list(phaseOrder)))

        return max(results)

    def SolvePartTwo(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        self.phases = [5, 6, 7, 8, 9]

        if not data:
            data = self.processed

        phaseOrderPermutations = itertools.permutations(self.phases, len(self.phases))

        results = []

        for phaseOrder in phaseOrderPermutations:
            amplifiers = self._initializeAmplifiers(data, amplifierClass=Day07ConcurrentComputer)
            results.append(self.testPhaseOrderConcurrent(amplifiers, list(phaseOrder)))

        return max(results)


def Main():
    solver = DaySolver07()
    solver.Run()


if __name__ == '__main__':
    Main()
