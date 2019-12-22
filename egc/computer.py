"""
Stores all the classes and functions we need to create a working Elf Guidance Computer
"""


class ParameterMode(object):
    Position = 0
    Immediate = 1


class EGCUnhandledOpcodeError(Exception):
    """
    Custom exception for raising an unknown opcode error in the event that the elf guidance computer encounters
    an opcode it doesn't known how to handle
    """
    def __init__(self, opcode, position):
        super(EGCUnhandledOpcodeError, self).__init__(
            "Ocode {} at position {} does not have a defined handler".format(opcode, position))


class EGCOutOfRangeError(Exception):
    """
    Custom exception for raising an issue if we attempt to access memory that is out of bounds
    of the current intbuffer
    """
    def __init__(self, index, bufferLength):
        super(EGCOutOfRangeError, self).__init__(
            "Attempted to access index {}, which is beyond the buffer size {}".format(index, bufferLength))


class ElfGuidanceComputer(object):
    """
    Base class for an Elf Guidance Computer based off the day02 intcode processor
    """
    def __init__(self, intBuffer, noun=None, verb=None):
        """
        :param list[int] intBuffer: The processed list of integers to use as our command and data buffer
        :param int noun: the address of the noun parameter
        :param int verb: the address of the verb parameter
        :param ParameterMode parameterMode: how we should handle the parameters of our commands
        """
        self.buffer = intBuffer

        self.buffer[1] = noun or intBuffer[1]
        self.buffer[2] = verb or intBuffer[2]

        self.currentIndex = 0
        self.finished = False

    def _add(self, argModeA, argModeB, argModeC):
        """
        Uses the computer's current position to add two numbers together and store the result
        at a third position determined by the input arg modes

        :returns int: the number of parameters used
        """
        a = b = 0

        if argModeA == ParameterMode.Position:
            a = self.buffer[self.buffer[self.currentIndex + 1]]
        elif argModeA == ParameterMode.Immediate:
            a = self.buffer[self.currentIndex + 1]

        if argModeB == ParameterMode.Position:
            b = self.buffer[self.buffer[self.currentIndex + 2]]
        elif argModeB == ParameterMode.Immediate:
            b = self.buffer[self.currentIndex + 2]

        c = a + b

        if argModeC == ParameterMode.Position:
            self.buffer[self.buffer[self.currentIndex + 3]] = c
        elif argModeC == ParameterMode.Immediate:
            raise EGCUnhandledOpcodeError("Parameters to which a function writes should not be Immediate", self.currentIndex)

        return 4

    def _mul(self, argModeA, argModeB, argModeC):
        """
        Uses the computer's current position to multiply two numbers together and store the result
        at a third position  determined by the input arg modes

        :returns int: the number of parameters used
        """
        a = b = 0

        if argModeA == ParameterMode.Position:
            a = self.buffer[self.buffer[self.currentIndex + 1]]
        elif argModeA == ParameterMode.Immediate:
            a = self.buffer[self.currentIndex + 1]

        if argModeB == ParameterMode.Position:
            b = self.buffer[self.buffer[self.currentIndex + 2]]
        elif argModeB == ParameterMode.Immediate:
            b = self.buffer[self.currentIndex + 2]

        c = a * b

        if argModeC == ParameterMode.Position:
            self.buffer[self.buffer[self.currentIndex + 3]] = c
        elif argModeC == ParameterMode.Immediate:
            raise EGCUnhandledOpcodeError("Parameters to which a function writes should not be Immediate", self.currentIndex)

        return 4

    def _store(self, argMode):
        """
        Takes one input and stores its value at the position specified

        :return int:
        """
        if argMode == ParameterMode.Position:
            self.buffer[self.buffer[self.currentIndex + 1]] = self.GetInput()
        if argMode == ParameterMode.Immediate:
            raise EGCUnhandledOpcodeError("Parameters to which a function writes should not be Immediate", self.currentIndex)

        return 2

    def GetInput(self):
        """
        Will need to be overwritten on a per-use basis

        :return: The thing input into the computer
        """
        raise EGCUnhandledOpcodeError("Input function not defined for this computer", self.currentIndex)

    def _retrieve(self, argMode):
        """
        Calls the computer's retrieve function using the input value as a parameter

        :param argMode: the paramter mode for the retrieval function

        :return int: the value at the given index
        """
        if argMode == ParameterMode.Position:
            self.Retrieve(self.buffer[self.buffer[self.currentIndex + 1]])
        if argMode == ParameterMode.Immediate:
            self.Retrieve(self.buffer[self.currentIndex + 1])

        return 2

    def Retrieve(self, value):
        """
        Will need to be overwritten on a per-use basis

        :param value: The value to be retrieved
        """
        raise EGCUnhandledOpcodeError("Output function not defined for this computer", self.currentIndex)

    def _complete(self):
        """
        Flips the "finished" bit
        """
        self.finished = True
        return 1

    def _processCurrentCommand(self):
        """
        Gets the current index and figures out what to do with the opcode at that index
        :return int: by how many addressess to advance the instruction pointer
        """
        # convert our opcode to a string so we can parse it and figure out what to do with it
        opcode = str(self.buffer[self.currentIndex]).zfill(5)

        instruction = int(opcode[-2:])

        print(self.currentIndex, instruction, opcode)

        if instruction == 1:
            argModeA = int(opcode[2])
            argModeB = int(opcode[1])
            argModeC = int(opcode[0])

            return self._add(argModeA, argModeB, argModeC)
        elif instruction == 2:
            argModeA = int(opcode[2])
            argModeB = int(opcode[1])
            argModeC = int(opcode[0])

            return self._mul(argModeA, argModeB, argModeC)
        elif instruction == 3:
            argMode = int(opcode[2])
            return self._store(argMode)
        elif instruction == 4:
            argMode = int(opcode[2])
            return self._retrieve(argMode)
        elif instruction == 5:
            return self._jumpIfTrue(int(opcode[2]), int(opcode[1]))
        elif instruction == 6:
            return self._jumpIfFalse(int(opcode[2]), int(opcode[1]))
        elif instruction == 7:
            return self._lessThan(int(opcode[2]), int(opcode[1]), int(opcode[0]))
        elif instruction == 8:
            return self._equals(int(opcode[2]), int(opcode[1]), int(opcode[0]))
        elif instruction == 99:
            return self._complete()
        else:
            raise EGCUnhandledOpcodeError(opcode, self.currentIndex)

    def _jumpIfTrue(self, argModeA, argModeB):
        """ if the first parameter is non-zero,
        it sets the instruction pointer to the value
        from the second parameter. Otherwise, it does nothing.

        :param argMode:
        :return:
        """
        a = 0
        b = 0

        if argModeA == ParameterMode.Position:
            a = self.buffer[self.buffer[self.currentIndex + 1]]
        elif argModeA == ParameterMode.Immediate:
            a = self.buffer[self.currentIndex + 1]

        if argModeB == ParameterMode.Position:
            b = self.buffer[self.buffer[self.currentIndex + 2]]
        elif argModeB == ParameterMode.Immediate:
            b = self.buffer[self.currentIndex + 2]

        if a != 0:
            self.currentIndex = b
            return 0

        return 3

    def _jumpIfFalse(self, argModeA, argModeB):
        """
        if the first parameter is zero,
        it sets the instruction pointer to the value
        from the second parameter.
        Otherwise, it does nothing.
        :param argMode:
        :return:
        """
        a = 0
        b = 0

        if argModeA == ParameterMode.Position:
            a = self.buffer[self.buffer[self.currentIndex + 1]]
        elif argModeA == ParameterMode.Immediate:
            a = self.buffer[self.currentIndex + 1]
        else:
            raise Exception("FAil")

        if argModeB == ParameterMode.Position:
            b = self.buffer[self.buffer[self.currentIndex + 2]]
        elif argModeB == ParameterMode.Immediate:
            b = self.buffer[self.currentIndex + 2]

        if a == 0:
            self.currentIndex = b
            return 0

        return 3

    def _lessThan(self, argModeA, argModeB, argModeC):
        """
        if the first parameter is less than the second parameter,
        it stores 1 in the position given by the third parameter.
        Otherwise, it stores 0.

        :param argModeA:
        :param argModeB:
        :param argModeC:

        :return:
        """
        a = 0
        b = 0

        if argModeA == ParameterMode.Position:
            a = self.buffer[self.buffer[self.currentIndex + 1]]
        elif argModeA == ParameterMode.Immediate:
            a = self.buffer[self.currentIndex + 1]

        if argModeB == ParameterMode.Position:
            b = self.buffer[self.buffer[self.currentIndex + 2]]
        elif argModeB == ParameterMode.Immediate:
            b = self.buffer[self.currentIndex + 2]

        c = 1 if a < b else 0

        if argModeC == ParameterMode.Position:
            self.buffer[self.buffer[self.currentIndex + 3]] = c
        elif argModeC == ParameterMode.Immediate:
            raise EGCUnhandledOpcodeError("Parameters to which a function writes should not be Immediate", self.currentIndex)

        return 4

    def _equals(self, argModeA, argModeB, argModeC):
        """
        if the first parameter is equal to the second parameter,
         it stores 1 in the position given by the third parameter.
          Otherwise, it stores 0.
        :param argModeA:
        :param argModeB:
        :return:
        """
        a = 0
        b = 0

        if argModeA == ParameterMode.Position:
            a = self.buffer[self.buffer[self.currentIndex + 1]]
        elif argModeA == ParameterMode.Immediate:
            a = self.buffer[self.currentIndex + 1]

        if argModeB == ParameterMode.Position:
            b = self.buffer[self.buffer[self.currentIndex + 2]]
        elif argModeB == ParameterMode.Immediate:
            b = self.buffer[self.currentIndex + 2]

        c = 1 if a == b else 0

        if argModeC == ParameterMode.Position:
            self.buffer[self.buffer[self.currentIndex + 3]] = c
        elif argModeC == ParameterMode.Immediate:
            raise EGCUnhandledOpcodeError("Parameters to which a function writes should not be Immediate", self.currentIndex)

        return 4

    def Run(self):
        """
        Runs the entire program in the buffer, starting at position 0
        """
        while not self.finished and self.currentIndex < len(self.buffer):
            output = self._processCurrentCommand()
            self.currentIndex += output

        if self.currentIndex > len(self.buffer) and not self.finished:
            raise EGCOutOfRangeError(self.currentIndex, len(self.buffer))

        print('Finished with index', self.currentIndex)
