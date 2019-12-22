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
            "Opcode {} at position {} does not have a defined handler".format(opcode, position))


class EGCUnexpectedParameterMode(Exception):
    def __init__(self, parameterMode, position):
        super(EGCUnexpectedParameterMode, self).__init__("Unexpected parameter mode {} at position {}".format(parameterMode, position))


class EGCAccessViolation(Exception):
    """
    Custom exception for raising an exception when an parameter attempts to write Immediately
    """
    def __init__(self, opcode, position):
        super(EGCAccessViolation, self).__init__(
            "Opcode {} at position {} cannot write in immediate mode".format(opcode, position))


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
        """
        self.buffer = intBuffer

        self.buffer[1] = noun or intBuffer[1]
        self.buffer[2] = verb or intBuffer[2]

        # state information
        self._parameterModes = []
        self.currentIndex = 0
        self.finished = False

        # initialize the input and output buffers
        self.input = None
        self.output = None

        # the maximum number of parameters for which we need to account
        self.maxParams = 5

    def _getValueForParameter(self, paramPosition):
        """
        Retrieves the value desired based on the instruction pointer
        and parameter mode for the given instruction

        :param int paramPosition: Where in the arg list to look for modes

        :return int: the value needed based on the parameter mode and position
        """
        mode = self._parameterModes[paramPosition]

        if mode == ParameterMode.Position:
           return self.buffer[self.buffer[self.currentIndex + 1 + paramPosition]]
        elif mode == ParameterMode.Immediate:
           return self.buffer[self.currentIndex + 1 + paramPosition]

        raise EGCUnexpectedParameterMode(mode, self.currentIndex)

    def _setValueForParameter(self, paramPosition, value):
        """
        Stores the value desired based on the instruction pointer
        and parameter mode for the given instruction

        :param int paramPosition: Where in the arg list to look for modes

        :return int: the value needed based on the parameter mode and position
        """
        # bail out if our param mode for storage is greater than 0
        if self._parameterModes[paramPosition]:
            raise EGCAccessViolation(self._parameterModes, self.currentIndex)

        # store the value using position mode
        self.buffer[self.buffer[self.currentIndex + paramPosition + 1]] = value

    def _add(self):
        """
        Uses the computer's current position to add two numbers together and store the result
        at a third position determined by the instructions arg modes

        :returns int: The number of parameters used in the instruction
        """
        a = self._getValueForParameter(0)
        b = self._getValueForParameter(1)

        self._setValueForParameter(2, a + b)

        return 4

    def _mul(self):
        """
        Uses the computer's current position to multiply two numbers together and store the result
        at a third position determined by the instructions arg modes

        :returns int: The number of parameters used in the instruction
        """
        a = self._getValueForParameter(0)
        b = self._getValueForParameter(1)

        self._setValueForParameter(2, a * b)

        return 4

    def _store(self):
        """
        Stores the result of the computer's GetInput function and stores its value at the position specified

        :returns int: The number of parameters used in the instruction
        """
        self._setValueForParameter(0, self.GetInput())

        return 2

    def GetInput(self):
        """
        Customizable input behavior based on the needs of the computer. By default, returns the value
        stored in the computer's input buffer

        :return: The value stored in the input buffer of the computer
        """
        return self.input

    def _output(self):
        """
        Calls the computer's Output function with the value deteremind by the opcodes parameter modes

        :returns int: The number of parameters used in the instruction
        """
        self.Output(self._getValueForParameter(0))

        return 2

    def Output(self, value):
        """
        Performs the output operation based on the spec of the computer, can be overriden

        :param value: The value to be stored in the output buffer
        """
        self.output = value

    def _jumpIfTrue(self):
        """
        if the value of the first parameter is non-zero,
        it sets the instruction pointer to the value
        from the second parameter.

        Otherwise, it advances the instruction pointer as normal

        :returns int: The number of parameters used in the instruction, or 0 if True
        """
        a = self._getValueForParameter(0)
        b = self._getValueForParameter(1)

        if a != 0:
            self.currentIndex = b
            return 0

        return 3

    def _jumpIfFalse(self):
        """
        If the value of the first parameter is 0
        it sets the instruction pointer to the value
        from the second parameter.

        Otherwise, it advances the instruction pointer as normal
        :param argMode:

        :returns int: The number of parameters used in the instruction, or 0 if False
        """
        a = self._getValueForParameter(0)
        b = self._getValueForParameter(1)

        if a == 0:
            self.currentIndex = b
            return 0

        return 3

    def _lessThan(self):
        """
        if the first parameter is less than the second parameter,
        it stores 1 in the position given by the third parameter.
        Otherwise, it stores 0.

        :returns int: The number of parameters used in the instruction
        """
        a = self._getValueForParameter(0)
        b = self._getValueForParameter(1)

        c = 1 if a < b else 0

        self._setValueForParameter(2, c)

        return 4

    def _equals(self):
        """
        if the first parameter is equal to the second parameter,
         it stores 1 in the position given by the third parameter.
          Otherwise, it stores 0.
        :param argModeA:
        :param argModeB:

        :returns int: The number of parameters used in the instruction
        """
        a = self._getValueForParameter(0)
        b = self._getValueForParameter(1)

        c = 1 if a == b else 0

        self._setValueForParameter(2, c)

        return 4

    def _complete(self):
        """
        Flips the "finished" bit

        :returns int: The number of parameters used in the instruction
        """
        self.finished = True
        return 1

    def _processCurrentCommand(self):
        """
        Gets the current index and figures out what to do with the opcode at that index
        :return int: by how many addressess to advance the instruction pointer
        """
        # convert our opcode to a string so we can parse it and figure out what to do with it
        opcode = str(self.buffer[self.currentIndex]).zfill(self.maxParams)

        instruction = int(opcode[-2:])

        # populate a state list of the parameter modes our functions may need
        self._parameterModes = [int(i) for i in opcode[:-2]][::-1]

        if instruction == 1:
            return self._add()
        elif instruction == 2:
            return self._mul()
        elif instruction == 3:
            return self._store()
        elif instruction == 4:
            return self._output()
        elif instruction == 5:
            return self._jumpIfTrue()
        elif instruction == 6:
            return self._jumpIfFalse()
        elif instruction == 7:
            return self._lessThan()
        elif instruction == 8:
            return self._equals()
        elif instruction == 99:
            return self._complete()

        raise EGCUnhandledOpcodeError(opcode, self.currentIndex)

    def Run(self):
        """
        Runs the entire program in the buffer, starting at position 0
        """
        while not self.finished and self.currentIndex < len(self.buffer):
            output = self._processCurrentCommand()
            self.currentIndex += output

        if self.currentIndex > len(self.buffer) and not self.finished:
            raise EGCOutOfRangeError(self.currentIndex, len(self.buffer))
