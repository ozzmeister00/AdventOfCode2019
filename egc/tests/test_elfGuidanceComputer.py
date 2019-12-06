from unittest import TestCase

from egc.computer import ElfGuidanceComputer, EGCUnhandledOpcodeError, EGCOutOfRangeError

import day02

class TestElfGuidanceComputer(TestCase):
    def setUp(self):
        super(TestElfGuidanceComputer, self).setUp()

        self.addTestProgram = [1, 0, 0, 0]
        self.mulTestProgram = [2, 0, 0, 0]
        self.completeTestProgram = [99]
        self.unknownCommandTestProgram = [-1]
        self.outOfRangeCommandTestProgram = [1, 0, 0, 0]
        self.sampleProgram = [1,0,0,0,2,4,4,4,99]

    def test__add(self):
        computer = ElfGuidanceComputer(self.addTestProgram)
        computer._add()
        self.assertEqual(computer.buffer[0], 2, msg="1 + 1 did not equal 2")

    def test__mul(self):
        computer = ElfGuidanceComputer(self.mulTestProgram)
        computer._mul()
        self.assertEqual(computer.buffer[0], 4, msg="2 * 2 did not equal 4")

    def test__complete(self):
        computer = ElfGuidanceComputer(self.completeTestProgram)
        computer._complete()
        self.assertTrue(computer.finished, msg="The computer did not properly execute a complete command")

    def test_unhandledOpcodeError(self):
        try:
            computer = ElfGuidanceComputer(self.unknownCommandTestProgram)
            computer._processCurrentCommand()
        except EGCUnhandledOpcodeError:
            self.assertTrue(True, msg="Successfully raised an unhandled opcode error")
        else:
            self.fail("We managed to operate on an unknown opcode")

    def test_outOfRangeError(self):
        try:
            computer = ElfGuidanceComputer(self.outOfRangeCommandTestProgram)
            computer.Run()
        except EGCOutOfRangeError:
            self.assertTrue(True, msg="Successfully raised an unhandled opcode error")

    def test_Run(self):
        computer = ElfGuidanceComputer(self.sampleProgram)
        computer.Run()

        self.assertTrue(computer.finished, msg="We did not successfully complete the sample program")

    def test_Day02(self):
        try:
            day02.Main()
        except:
            self.fail(msg="Something went wrong testing day 2")



