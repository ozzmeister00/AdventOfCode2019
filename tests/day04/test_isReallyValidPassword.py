from unittest import TestCase

from day04 import IsReallyValidPassword


class TestIsReallyValidPassword(TestCase):
    def test_IsReallyValidPassword(self):
        self.assertTrue(IsReallyValidPassword(112233), msg="112233 should be a valid password")
        self.assertFalse(IsReallyValidPassword(123444), msg="123444 should not be a valid password")
        self.assertTrue(IsReallyValidPassword(111122), msg="111122 should not be a valid password")

