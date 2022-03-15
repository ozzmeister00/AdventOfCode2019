"""
10
"""
import math

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
        self.testDataPartTwo = {'''.#..##.###...#######
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
###.##.####.##.#..##''':802}

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
        # TODO: Get vector to each asteroid and then check if there are more than one asteroids on the same vector

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
            sx = 28
            sy = 29
            data = self.processed
        else:
            sx = 11
            sy = 13

        grid = data.copy()

        startPoint = Float2([sx, sy])

        countedHits = 0
        totalHits = []

        rays = 360
        step = 1  # keep it nice and granular

        oneEightyOverPi = 180 / math.pi

        height = len(grid)
        width = len(grid[0])

        radius = max(height, width)

        hitX = hitY = -1

        # the whole list of asteroids
        asteroidDB = {}
        for y in range(height):
            for x in range(width):
                if grid[y][x]:
                    asteroidDB[(x, y)] = True

        # print('11x14', grid[14][11])

        grid[14][11] = 2

        passCount = 0

        # TODO we're registering hits in places we shouldn't, like it's working it's way back to front
        # but we're also not clicking what should be our blocking hits

        while countedHits < 200 and passCount < 10:
            passCount += 1
            # do a pass of 360 degrees and collect the asteroids we'll hit
            endPoint = Float2([sx, sy])

            passHits = []

            print("Pass")

            flat = []
            for i in grid:
                flat += i

            # for each degree in 360 degrees
            for i in range(0, rays + 1, step):
                ax = math.sin(i / oneEightyOverPi)
                ay = math.cos(i / oneEightyOverPi)

                # step out from the origin
                for z in range(radius):
                    endPoint.x += ax
                    endPoint.y += ay

                    # print(startPoint, endPoint)

                    # end our ray if we're our of bounds
                    if endPoint.x < 0 or endPoint.y < 0 or endPoint.x >= width or endPoint.y >= width:
                        # print("Ending ray because out of bounds")
                        break

                    tX = int(round(endPoint.x))
                    tY = int(round(endPoint.y))

                    if tX < 0 or tY < 0 or tX >= width or tY >= height:
                        # print("Ending ray because out of bounds")
                        break

                    # print(tX, tY)
                    #
                    # print(grid[tY][tX], (tX, tY) in passHits)

                    # if we've hit an asteroid that we haven't already hit
                    if grid[tY][tX] == 1 and (tX, tY) not in passHits:
                        # make sure there wasn't somehow another asteroid in the way

                        # get the point of the asteroid we can see along the given ray
                        tPoint = Float2([tX, tY])

                        edge = Edge(startPoint, tPoint)
                        safe = True

                        # test all of the remaining active asteroids and see if they're on the line between our base
                        # station and the hit asteroid
                        for aPoint in [aPoint for aPoint in asteroidDB if asteroidDB[aPoint]]:
                            aFloat2 = Float2(aPoint)
                            # if we're not looking at the start or end asteroids
                            if aFloat2 != startPoint and aFloat2 != tPoint:
                                if edge.PointOnEdge(aFloat2):
                                    #print(aFloat2, "is on edge between ", startPoint, tPoint)
                                    safe = False
                                    break

                        # if we passed our test, add the point to the list of hit points
                        if safe:
                            passHits.append((tX, tY))
                            grid[tY][tX] = 3
                            countedHits += 1
                            print("Found a hit at", tX, tY, countedHits)
                            break

                # if we hit 200 before breaking out of the 360 pass, bail out of the pass so we can bail out of the while loop
                if countedHits > 199:
                    break

            # after a pass is over, flip the asteroids we hit
            for aX, aY in passHits:
                #grid[aY][aX] = 0
                asteroidDB[(aX, aY)] = False
                totalHits.append((aX, aY))

            for line in grid:
                print(line)

        hitX, hitY = totalHits[-1]

        # figure out how far away we should check
        # for each "pass"
        # determine the angle to each first-hit asteroid
        # sort the asteroid angles into a "pass"
        # destroy each asteroid in the path
        # advance to the next asteroid in angle order
        # once we get around to the top, reevaluate the pass

        return (hitX * 100) + hitY


    def Run(self):
        # Overriding the run method because part 1 is unoptimized
        print('TestResult2:', self.TestAlgorithm(self.SolvePartTwo, part=2))
        print('Result: ', self.SolvePartTwo())


def Main():
    solver = DaySolver10()
    solver.Run()


if __name__ == '__main__':
    Main()        