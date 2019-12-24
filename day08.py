"""
08
"""

from utils.solver import ProblemSolver


class DaySolver08(ProblemSolver):
    def __init__(self):
        super(DaySolver08, self).__init__(8)

        self.testDataPartOne = {('123456789012', (3, 2)): 1}
        self.testDataPartTwo = {('0222112222120000', (2, 2)): '\n 1\n1 '}

    def ProcessInput(self, data=None):
        """
        :param str data: the pixel encoding of the
        """
        if not data:
            # add in the size of our final image if we're not working with overriden data
            data = [self.rawData]
            data.append((25, 6))

        processed = [[int(i) for i in data[0]], data[1]]

        return processed

    def UnpackIntoLayers(self, pixels, layerSize):
        """
        Given the input pixel stream, break it up
        into separate layers based on the number of
        pixels in a layer

        :param list[int] pixels: the raw pixel stream
        :param int layerSize: the number of pixels in a layer

        :return list[list[int]]: the image broken up into layers
        """
        image = []

        for i, value in enumerate(pixels):
            # if we've reached the end of the count, add a layer
            if i % layerSize == 0:
                image.append([])

            # then add the current value to the current layer
            image[-1].append(value)

        return image

    def SolvePartOne(self, data=None):
        """
        :param list[int] data: the stream of pixel values to test
        
        :return int: the number of twos * the number of ones in the layer with the fewest zeroes
        """
        if not data:
            data = self.processed

        # break apart our input data struct
        width = data[1][0]
        height = data[1][1]
        pixels = data[0]

        # how many pixels in each layer
        imageSize = width * height

        image = self.UnpackIntoLayers(pixels, imageSize)

        # get a count of zeroes in each layer
        zeroCount = []
        for layer in image:
            zeroCount.append(layer.count(0))

        # then find the layer with the fewest zeroes
        fewestZeroesValue = min(zeroCount)
        fewestZeroesIndex = zeroCount.index(fewestZeroesValue)

        ones = image[fewestZeroesIndex].count(1)
        twos = image[fewestZeroesIndex].count(2)

        return ones * twos

    def SolvePartTwo(self, data=None):
        """
        :param list[int] data: the stream of pixel values to test
        
        :return string: the final image, with 1s present and zeros as spaces
        """
        if not data:
            data = self.processed

        width = data[1][0]
        height = data[1][1]
        pixels = data[0]

        # how many pixels in each layer
        imageSize = width * height

        layers = self.UnpackIntoLayers(pixels, imageSize)

        # first, resolve the pixels at each position in the layers
        # starting with the backmost layer
        finalImage = layers[-1]

        # then, working back to front starting with the penultimate layer
        for layer in layers[-2::-1]:
            for i, value in enumerate(layer):
                if value != 2:
                    finalImage[i] = value

        # then resolve our image into a string delimited by newline characters at the end of each row
        outString = ''
        for i, value in enumerate(finalImage):
            if i % width == 0:
                outString += '\n'

            # only output a number 1, and leave the zeroes as spaces so our poor human eyes can resolve the code
            outString += str(value) if value else ' '

        return outString


def Main():
    solver = DaySolver08()
    solver.Run()


if __name__ == '__main__':
    Main()
