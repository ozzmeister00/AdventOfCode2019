"""
5
"""

from utils.solver import ProblemSolver

from egc.computer import ElfGuidanceComputer


class Day05Computer(ElfGuidanceComputer):
    def GetInput(self):
        return 5

    def Retrieve(self, value):
        """

        :param value:
        :return:
        """
        print('Output:', value)


class DaySolver05(ProblemSolver):
    def __init__(self):
        super(DaySolver05, self).__init__(5)

        self.testDataPartOne = {'3,0,4,0,99': None}
        self.testDataPartTwo = {}

    def ProcessInput(self, data=None):
        """
        :param str data:
        """
        if not data:
            data = self.rawData

        processed = [int(i) for i in data.split(',')]

        return processed

    def SolvePartOne(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        if not data:
            data = self.processed

        computer = Day05Computer(data)
        computer.Run()

    def SolvePartTwo(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        if not data:
            data = self.processed


def Main():
    solver = DaySolver05()
    solver.Run()


if __name__ == '__main__':
    Main()
