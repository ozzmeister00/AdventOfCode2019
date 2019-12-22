"""
5
"""

from utils.solver import ProblemSolver

from egc.computer import ElfGuidanceComputer


class Day05Part01Computer(ElfGuidanceComputer):
    """
    Day 05 Part 01 EGC that warns if the output value is not 0
    """
    def Retrieve(self, value):
        super(Day05Part01Computer, self).Retrieve(value)

        if value != 0:
            print("Value", value, "is not 0")


class DaySolver05(ProblemSolver):
    def __init__(self):
        super(DaySolver05, self).__init__(5)

        self.testDataPartOne = {'3,0,4,0,99': 1}
        self.testDataPartTwo = {'3,9,8,9,10,9,4,9,99,-1,8': 0,
                                '3,9,7,9,10,9,4,9,99,-1,8':1,
                                '3,3,1108,-1,8,3,4,3,99':0,
                                '3,3,1107,-1,8,3,4,3,99':1,
                                '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9':1,
                                '3,3,1105,-1,9,1101,0,0,12,4,12,99,1':1,
                                '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99':999}

    def ProcessInput(self, data=None):
        """
        Take the input data and parse it into a list of strings

        :param str data:

        :returns list[int]: the current memory buffer
        """
        if not data:
            data = self.rawData

        processed = [int(i) for i in data.split(',')]

        return processed

    def SolvePartOne(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result, which is the value stored in the EGC's output buffer
        """
        if not data:
            data = self.processed

        computer = Day05Part01Computer(data)
        computer.input = 1
        computer.Run()

        return computer.output

    def SolvePartTwo(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the EGC's output buffer at the end of program execution
        """
        if not data:
            # re instantiate the buffer from raw data, for safety
            data = self.ProcessInput(self.rawData)

        computer = ElfGuidanceComputer(data)
        computer.input = 5
        computer.Run()

        return computer.output


def Main():
    solver = DaySolver05()
    solver.Run()


if __name__ == '__main__':
    Main()
