"""
Stores all the classes and functions we need to create a working Elf Guidance Computer
"""


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
        """
        self.buffer = intBuffer

        self.buffer[1] = noun or intBuffer[1]
        self.buffer[2] = verb or intBuffer[2]

        self.currentIndex = 0
        self.finished = False

    def _add(self):
        """
        Uses the computer's current position to add two numbers together and store the result
        at a third position

        index of first value = index + 1
        index of second value = index + 2
        index at which to store the result = index + 3

        :returns int: the number of parameters used
        """
        a = self.buffer[self.buffer[self.currentIndex + 1]]
        b = self.buffer[self.buffer[self.currentIndex + 2]]
        c = a + b
        self.buffer[self.buffer[self.currentIndex + 3]] = c

        return 4

    def _mul(self):
        """
        Uses the computer's current position to multiply two numbers together and store the result
        at a third position

        index of first value = index + 1
        index of second value = index + 2
        index at which to store the result = index + 3

        :returns int: the number of parameters used
        """
        a = self.buffer[self.buffer[self.currentIndex + 1]]
        b = self.buffer[self.buffer[self.currentIndex + 2]]
        c = a * b
        self.buffer[self.buffer[self.currentIndex + 3]] = c

        return 4

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
        opcode = self.buffer[self.currentIndex]

        print(self.currentIndex, opcode)

        if opcode == 1:
            return self._add()
        elif opcode == 2:
            return self._mul()
        elif opcode == 99:
            return self._complete()
        else:
            raise EGCUnhandledOpcodeError(opcode, self.currentIndex)

    def Run(self):
        """
        Runs the entire program in the buffer, starting at position 0
        """
        while not self.finished and self.currentIndex < len(self.buffer):
            self.currentIndex += self._processCurrentCommand()

        if self.currentIndex > len(self.buffer) and not self.finished:
            raise EGCOutOfRangeError(self.currentIndex, len(self.buffer))
