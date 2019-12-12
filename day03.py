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


class Edge(object):
    def __init__(self, start, end):
        """

        :param Float2 start:
        :param Float2 end:
        """
        self.start = start
        self.end = end

    def GetLength(self):
        """
        :return integer: the Manhattan distance length of the line
        """
        return abs((self.end.x - self.start.x) + (self.end.y - self.start.y))

    def EdgeInBounds(self, otherEdge):
        # other edge starts in bounds
        if True:  # TODO
            return True

        return False

    def FindIntersection(self, otherEdge):
        return Float2([0,0])


class DaySolver03(ProblemSolver):
    def __init__(self):
        super(DaySolver03, self).__init__(3)

        self.testDataPartOne = {'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83': 159,
                                'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7': 135
                                }
        self.testDataPartTwo = {}

    def ProcessInput(self, data=None):
        """
        :param str data: breaking the directions down into [(Direction, Distance)]
        """
        if not data:
            data = self.rawData

        # split out the wires, and for each wire split out Direction, Distance
        processed = [[(i[0], int(i[1:])) for i in line.split(',')] for line in data.split('\n')]

        return processed

    def SolvePartOne(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        if not data:
            data = self.processed

        wires = [[], []]

        #   figure out each of the "edges" of the wire based on the start, and next point
        for index, wire in enumerate(data):
            currentPoint = Float2([0, 0])
            for direction, distance in wire:
                newPoint = Float2([currentPoint + Directions[direction]])
                edge = Edge(currentPoint, newPoint)
                wires[index].append(edge)
                currentPoint = newPoint

        intersections = []

        # then compare each edge against each edge in the other wire for intersection
        for edgeA in wires[0]:
            for edgeB in wires[1]:
                # check the bounding boxes of each wire
                intersection = edgeA.FindIntersection(edgeB)  # TODOzd
                if intersection:
                    intersections.append(intersection)

        # store the intersections, then do manhattan distance and find the shortest distance
        intersectDistances = []
        for intersect in intersections:
            intersectDistances.append(abs(intersect.x) + abs(intersect.y))

        minValue = min(intersectDistances)

        return minValue

    def SolvePartTwo(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        if not data:
            data = self.processed


def Main():
    solver = DaySolver03()
    solver.Run()


if __name__ == '__main__':
    Main()
