"""
--- Day 3: Crossed Wires ---
The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back on
 Earth, the fuel management system wasn't completely installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend
outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of text
(your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the
intersection point closest to the central port. Because the wires are on a grid, use the Manhattan distance for
 this measurement. While the wires do technically cross right at the central port where they both start, this point
  does not count, nor does a wire count as crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8, up 5,
left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........
Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
These wires cross at two locations (marked X),
 but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
What is the Manhattan distance from the central port to the closest intersection?
"""

import math

from utils.solver import ProblemSolver
from utils.math import Float2


Directions = {'R': Float2([1, 0]),
             'L': Float2([-1, 0]),
             'U': Float2([0, 1]),
             'D': Float2([0, -1])}


class Orientations(object):
    Colinear = 0
    Clockwise = 1
    Counterclockwise = 2


class Edge(object):
    def __init__(self, start, end):
        """

        :param Float2 start: Where the edge starts
        :param Float2 end: Where the edge ends
        """
        self.start = start
        self.end = end

    def __str__(self):
        return '{}, {}'.format(self.start, self.end)

    def GetLength(self):
        """
        :return int: the Manhattan distance length of the line
        """
        return abs((self.end.x - self.start.x) + (self.end.y - self.start.y))

    def PointOnEdge(self, point):
        """
        Given an input point, determine if the point is colinear and within the bounds
        of the edge

        :param Float2 point:
        :return bool: if the point is on the line
        """
        # if the point is colinear, and within the bounding box of our edge, then
        # it must be on the line
        if self.GetOrientationWithOtherPoint(point) == Orientations.Colinear:
            if self.PointInBounds(point):
                return True

        return False

    def PointInBounds(self, point):
        """
        Given input point that is colinear with this edge, determine if the point
        is on the segment

        :param Float2 point:
        :return bool:
        """
        if point.x <= max(self.start.x, self.end.x) and \
           point.x >= min(self.start.x, self.end.x) and \
           point.y <= max(self.start.y, self.end.y) and \
           point.y >= min(self.start.y, self.end.y):
            return True

        return False

    def GetOrientationWithOtherPoint(self, point):
        """
        # To find orientation of ordered triplet (p, q, r).
        # The function returns following values
        # 0 --> p, q and r are colinear
        # 1 --> Clockwise
        # 2 --> Counterclockwise
        static int orientation(Point p, Point q, Point r)
        {

        }
        :param Float2 point:
        :return:
        """
        value = (point.y - self.start.y) * (self.end.x - point.x) - (point.x - self.start.x) * (self.end.y - point.y)

        if not value:
            return Orientations.Colinear
        elif value > 0:
            return Orientations.Clockwise
        else:
            return Orientations.Counterclockwise

    def DoesIntersect(self, otherEdge):
        """

        :param Edge otherEdge:
        :return bool:
        """
        # determine the orientations using all possible permutations
        o1 = self.GetOrientationWithOtherPoint(otherEdge.start)
        o2 = self.GetOrientationWithOtherPoint(otherEdge.end)
        o3 = otherEdge.GetOrientationWithOtherPoint(self.start)
        o4 = otherEdge.GetOrientationWithOtherPoint(self.end)

        # if the orientations of triangles created by each of the points of the segment
        # do not match, then we intersect
        if o1 != o2 and o3 != o4:
            return True

        # if segments are colinear
        if o1 == Orientations.Colinear and self.PointInBounds(otherEdge.start):
            return True
        if o2 == Orientations.Colinear and self.PointInBounds(otherEdge.end):
            return True
        if o3 == Orientations.Colinear and otherEdge.PointInBounds(self.start):
            return True
        if o4 == Orientations.Colinear and otherEdge.PointInBounds(self.end):
            return True

        return False

    def FindIntersection(self, otherEdge):
        """
        Finds the point at which this edge and the input otherEdge intersect, if at all

        :param Edge otherEdge:
        :return Float2: the point of intersection
        """
        if self.DoesIntersect(otherEdge):
            xdiff = Float2([self.start.x - self.end.x, otherEdge.start.x - otherEdge.end.x])
            ydiff = Float2([self.start.y - self.end.y, otherEdge.start.y - otherEdge.end.y])

            def det(a, b):
                return a.x * b.y - a.y * b.x

            div = det(xdiff, ydiff)
            if not div:
                return False

            d = Float2([det(self.start, self.end), det(otherEdge.start, otherEdge.end)])
            x = det(d, xdiff) / div
            y = det(d, ydiff) / div
            return Float2([x, y])

        return False


class DaySolver03(ProblemSolver):
    def __init__(self):
        super(DaySolver03, self).__init__(3)

        self.testDataPartOne = {'R8,U5,L5,D3\nU7,R6,D4,L4': 6,
                                'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83': 159,
                                'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7': 135
                                }
        self.testDataPartTwo = {'R8,U5,L5,D3\nU7,R6,D4,L4': 30,
                                'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83': 610,
                                'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7': 410
                                }

    def ProcessInput(self, data=None):
        """
        :param str data: breaking the directions down into [(Direction, Distance)]
        """
        if not data:
            data = self.rawData

        # split out the wires, and for each wire split out Direction, Distance
        processed = [[(i[0], int(i[1:])) for i in line.split(',')] for line in data.split('\n')]

        return processed

    def BuildWire(self, wire):
        """
        Build a list of edges that constitue the input wire directions
        :param list wire:
        :return list[Edge]:
        """
        output = []

        currentPoint = Float2([0, 0])
        for direction, distance in wire:
            newPoint = currentPoint + (Directions[direction] * distance)
            edge = Edge(currentPoint, newPoint)
            output.append(edge)
            currentPoint = newPoint

        return output

    def BuildWires(self, data):
        """

        :param data:
        :return:
        """
        wires = [[], []]

        #   figure out each of the "edges" of the wire based on the start, and next point
        for index, wire in enumerate(data):
            wires[index] = self.BuildWire(wire)

        return wires

    def GetWireIntersections(self, wires):
        """
        Loop over all the edges in each wire and determine their points of intersection

        :param list wires:
        :return list: the points at which the wires intersect
        """
        intersections = []

        # then compare each edge against each edge in the other wire for intersection
        for edgeA in wires[0]:
            for edgeB in wires[1]:
                # check the bounding boxes of each wire
                intersection = edgeA.FindIntersection(edgeB)
                if intersection and (intersection.x != 0.0 and intersection.y != 0.0):
                    intersections.append(intersection)

        return intersections

    def SolvePartOne(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        if not data:
            data = self.processed

        wires = self.BuildWires(data)

        intersections = self.GetWireIntersections(wires)

        assert len(intersections) > 0, "We didn't find any intersections"

        # store the intersections, then do manhattan distance and find the shortest distance
        intersectDistances = []
        for intersect in intersections:
            intersectDistances.append(abs(intersect.x) + abs(intersect.y))

        minValue = min(intersectDistances)

        return minValue

    def SolvePartTwo(self, data=None):
        """
        Loop over all the intersections in the wires and determine the distance
        to each that intersect point for each wire and use that to determine the shortest distance

        :param list data: the data to operate on
        
        :return : the result
        """
        if not data:
            data = self.processed

        wires = self.BuildWires(data)

        intersections = self.GetWireIntersections(wires)

        intersectDistances = []
        for intersection in intersections:
            intersectDistances.append(sum([self.tracePathToIntersection(wire, intersection) for wire in wires]))

        minValue = min(intersectDistances)

        return minValue

    def tracePathToIntersection(self, wire, intersection):
        """

        :param list[Edge] wire:
        :param Float2 intersection:
        :return float: the total driving distance to reach the intersection on this wire
        """
        distance = 0.0
        for edge in wire:
            if edge.PointInBounds(intersection):
                partialEdge = Edge(edge.start, intersection)
                distance += partialEdge.GetLength()
                break
            else:
                distance += edge.GetLength()

        return distance


def Main():
    solver = DaySolver03()
    solver.Run()


if __name__ == '__main__':
    Main()
