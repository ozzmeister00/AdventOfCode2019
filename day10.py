"""
10
"""

from utils.solver import ProblemSolver
from utils.math import Float2
from day03 import Edge


class DaySolver10(ProblemSolver):
    def __init__(self):
        super(DaySolver10, self).__init__(10)

        self.testDataPartOne = {'''.#..#
.....
#####
....#
...##''':8,
                                '''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####''':33,
                                '''#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.''':35,
                                '''.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..''':41,
                                '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##''':210}
        self.testDataPartTwo = {}

    def ProcessInput(self, data=None):
        """
        :param str data:

        :returns list[list[int]]: the grid of 1s and 0s to represent the asteroid field
        """
        if not data:
            data = self.rawData

        processed = []
        for line in data.split('\n'):
            newLine = []
            for i in line:
                if i == '#':
                    newLine.append(1)
                else:
                    newLine.append(0)
            processed.append(newLine)

        return processed

    def testFromSpot(self, x, y, grid, asteroidDB):
        """
        :param int x: the x coord to start from
        :param int y: the y coord to start from
        :param list[list[int] grid: the map we're testing with
        :param list[tuple(int, int)] asteroidDB: the database of (x, y): bool asteroids we know about

        :return int: the number of detectable asteroids from the given x, y coordinate
        """
        # init the asteroidDB as a db of Falses so we can track which asteroids we hit
        asteroidDB = {k: False for k in asteroidDB}

        height = len(grid)
        width = len(grid[0])

        hits = [[0] * width for i in range(height)]

        startPoint = Float2([x, y])

        for tx, ty in asteroidDB:
            endPoint = Float2([tx, ty])
            safe = True
            if endPoint != startPoint:
                edge = Edge(startPoint, endPoint)
                for ax, ay in asteroidDB:
                    # don't test our target point, or our start point
                    tPoint = Float2([ax, ay])
                    if tPoint != startPoint and tPoint != endPoint:
                        if edge.PointOnEdge(tPoint):
                            safe = False
                            break

                if safe:
                    asteroidDB[(tx, ty)] = True
                    hits[ty][tx] = 1

        # for line in hits:
        #     print(line)

        hitAsteroids = list(asteroidDB.values()).count(True)

        return hitAsteroids

    def SolvePartOne(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        print("Running test")
        if not data:
            data = self.processed

        # store hit results in a grid ready to accumulate
        results = [[0] * len(line) for line in data]

        asteroids = []

        # loop over each spot in the map
        for y in range(len(data)):
            for x in range(len(data[y])):
                # if we're on an asteroid, stash off its location
                if data[y][x]:
                    asteroids.append((x, y))

        for x, y in asteroids:
            results[y][x] = self.testFromSpot(x, y, data, asteroids)

        for line in results:
            print(line)

        # condense results
        flatResults = []
        for line in results:
            for i in line:
                flatResults.append(i)

        return max(flatResults)

    def SolvePartTwo(self, data=None):
        """
        :param list data: the data to operate on
        
        :return : the result
        """
        if not data:
            data = self.processed


def Main():
    solver = DaySolver10()
    solver.Run()


if __name__ == '__main__':
    Main()        