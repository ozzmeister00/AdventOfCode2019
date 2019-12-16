from unittest import TestCase

from day04 import IsValidPassword


class TestIsValidPassword(TestCase):
    def test_IsValidPassword(self):
        self.assertTrue(IsValidPassword(111111), msg="111111 should be a valid password")
        self.assertFalse(IsValidPassword(223450), msg="223450 should not be a valid password")
        self.assertFalse(IsValidPassword(123789), msg="123789 should not be a valid password")
