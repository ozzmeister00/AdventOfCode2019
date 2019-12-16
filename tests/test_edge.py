from unittest import TestCase

from utils.math import Float2
from day03 import Edge

class TestEdge(TestCase):
    def test_GetLength(self):
        start = Float2([0, 0])
        end = Float2([0, 10])
        edge = Edge(start, end)

        self.assertEqual(edge.GetLength(), 10, msg="Our edge of length 10 did not say it was length 10")

    def test_DoesIntersect(self):
        start = Float2([-5, 0])
        end = Float2([5, 0])
        edgeA = Edge(start, end)

        start = Float2([0, -5])
        end = Float2([0, 5])
        edgeB = Edge(start, end)

        self.assertTrue(edgeA.DoesIntersect(edgeB), msg="Our edges that should intersect didn't")

    def test_FindIntersection(self):
        start = Float2([-5, 0])
        end = Float2([5, 0])
        edgeA = Edge(start, end)

        start = Float2([0, -5])
        end = Float2([0, 5])
        edgeB = Edge(start, end)

        target = Float2([0.0, 0.0])
        intersection = edgeA.FindIntersection(edgeB)

        self.assertEquals(intersection, target, msg="Our intersecting point is not what it should be")

