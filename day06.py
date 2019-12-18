import collections
import math


from utils.solver import ProblemSolver


class Day06Solver(ProblemSolver):
    def __init__(self):
        super(Day06Solver, self).__init__(6)

        self.testDataPartOne = {"""COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""":42}

        self.testDataPartTwo = {"""COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""":4}

    def ProcessInput(self, data=None):
        """
        :param str data:

        :return dict: relation map of body: orbited body inverting the test data we brought in
        """
        if not data:
            data = self.rawData

        processed = {}

        for line in data.split('\n'):
            orbit, body = line.split(')')
            processed[body] = orbit

        return processed

    def SolvePartOne(self, data=None):
        """
        :param list data:
        :return int: the number of direct and indirect orbits
        """
        if not data:
            data = self.processed

        orbits = 0

        # for each body, trace down the map until we arrive at the COM
        for body in data:
            currentBody = body
            while currentBody != 'COM':
                currentBody = data[currentBody]
                orbits += 1

        return orbits

    def SolvePartTwo(self, data=None):
        """
        :param list data:
        :return :
        """
        if not data:
            data = self.processed

        steps = 0
        you = 'YOU'
        san = 'SAN'

        # build out the map from top down off our bottom up
        outwardMap = collections.defaultdict(list)
        for child, parent in data.items():
            outwardMap[parent].append(child)

        # build a path toward the core from our current position
        def inward(current, path):
            path.append(current)
            current = data[current]

            if current != 'COM':
                current, path = inward(current, path)

            return current, path

        _, youToCore = inward('YOU', [])
        _, santaToCore = inward('SAN', [])

        youToCore = set(youToCore)
        santaToCore = set(santaToCore)
        santaToTrunk = santaToCore.difference(youToCore)
        youToTrunk = youToCore.difference(santaToCore)

        totalPath = list(santaToTrunk.union(youToTrunk))

        # remove YOU and SAN from the path we took
        pathLength = len(totalPath) - 2

        return pathLength

if __name__ == '__main__':
    Day06Solver = Day06Solver()
    Day06Solver.Run()
