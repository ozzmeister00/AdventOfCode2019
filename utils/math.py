"""
Common maths functions and datatypes for solving Advent of Code problems
"""

import functools
import operator


def product(iterable):
    """
    Returns the product of an iterable of numbers
    :param list iterable: eg [1, 2, 3, 4, 5]
    :return float: the product of all items in the iterable multiplied together
    """
    return functools.reduce(operator.mul, iterable, 1)


class Float2(list):
    """
    A Float2 object to make it easier to access and multiply 2-length lists of numbers
    """
    def __init__(self, inV):
        """

        :param list inV: two-length list of numbers
        """
        inV = [float(v) for v in inV]  # convert our inputs to floats
        super(Float2, self).__init__(inV)

    def __add__(self, other):
        return Float2([self.x + other.x, self.y + other.y])

    def __sub__(self, other):
        return Float2([self.x - other.x, self.y - other.y])

    def __mul__(self, other):
        if isinstance(other, Float2):
            return Float2([self.x * other.x, self.y * other.y])
        if isinstance(other, int) or isinstance(other, float):
            return Float2([self.x * other, self.y * other])

    def __eq__(self, other):
        if isinstance(other, Float2):
            if self.x == other.x and self.y == other.y:
                return True

        return False

    @property
    def x(self):
        """
        Access the first, X value of the list
        :return float:
        """
        return self[0]

    @x.setter
    def x(self, v):
        self[0] = v

    @property
    def y(self):
        """
        The second, Y value of the list
        :return float:
        """
        return self[1]

    @y.setter
    def y(self, v):
        self[1] = v


def dot(a, b):
    """
    :param list a: list of numbers
    :param list b: list of numbers equal in length to the first list
    :return float: dot product of n-length lists of numbers
    """
    if len(a) != len(b):
        raise ValueError("Input lists must be of equal length (got {} and {})".format(len(a), len(b)))

    return sum([x * y for x, y in zip(a, b)])


def getBarycentric(p, a, b, c):
    """
    Get the barycentric coordinates of cartesin point a in
    reference frame abc

    :param Float2 p: test point
    :param Float2 a: point A
    :param Float2 b: point B
    :param Float2 c: point C

    :return list: the UVW coordinate of cartesian point P in reference frame created by points ABC
    """
    v0 = b - a  # Vector BA
    v1 = c - a  # Vector CA
    v2 = p - a  # Vector PA
    d00 = dot(v0, v0)  # dot BA . BA
    d01 = dot(v0, v1)  # dot BA . CA
    d11 = dot(v1, v1)  # dot CA . CA
    d20 = dot(v2, v0)  # dot PA . BA
    d21 = dot(v2, v1)  # dot PA . CA

    denom = (d00 * d11) - (d01 * d01)

    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w

    return u, v, w
