"""
09
"""

from egc.computer import ExtraMemoryComputer
from utils.solver import ProblemSolver


class Day09Computer(ExtraMemoryComputer):
    """
    The Day09 computer should treat its output as a list buffer
    """
    def __init__(self, *args, **kwargs):
        super(Day09Computer, self).__init__(*args, **kwargs)

        self.output = []

    def Output(self, value):
        """
        Append the value to the output buffer

        :param int value: the value to store
        """
        self.output.append(value)


class DaySolver09(ProblemSolver):
    def __init__(self):
        super(DaySolver09, self).__init__(9)

        self.testDataPartOne = {'1102,34915192,34915192,7,4,7,99,0':1219070632396864,
                                '104,1125899906842624,99':1125899906842624}
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

        computer = Day09Computer(data)
        computer.input = 1

        computer.Run()

        if len(computer.output) > 1:
            print(computer.output)
            print("Output buffer was bigger than expected")

        return computer.output[-1]

    def SolvePartTwo(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        if not data:
            data = self.processed

        computer = Day09Computer(data)
        computer.input = 2

        computer.Run()

        if len(computer.output) > 1:
            print(computer.output)
            print("Output buffer was bigger than expected")

        return computer.output[-1]

def Main():
    solver = DaySolver09()
    solver.Run()


if __name__ == '__main__':
    Main()
