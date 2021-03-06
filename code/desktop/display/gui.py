from display import *
from graphics import GraphWin, Point, Polygon
from numpy import array as arr
import math
import asyncio

segmentWidth = 150          # how fat the segments are
shortSegmentLength = 803    # the length of horizontal/vertical segments
longSegmentLength = 905     # the length of diagonal segments
rootTwo = math.sqrt(2)      # useful mathematical constant

# half of the above values (avoids * 0.5 everywhere)
halfSegmentWidth = segmentWidth * 0.5
halfShortSegmentLength = shortSegmentLength * 0.5
halfLongSegmentLength = longSegmentLength * 0.5
halfRootTwo = rootTwo * 0.5

spacing = 30        # the spacing between segments
diagonalSpacing = spacing * halfRootTwo # the spacing where diagonal points meet (spacing at 45 degree angle)
twiceDiagonalSpacing = diagonalSpacing * 2.0

# radius includes single imaginary spacing gap around the character and interior diagonal spacing between segments
characterRadius = shortSegmentLength + halfSegmentWidth + spacing + diagonalSpacing
characterDiameter = characterRadius * 2
characterGap = 1362

lineHeight = characterDiameter + characterRadius
kerning = characterDiameter + characterRadius


scale = 0.036        # the scale to transfer mm into pixels

def normaliseColor(color):
    '''Handle colors specified as arrays of rgb numbers, and translate to Tk color strings'''
    colorType = type(color)
    if colorType is str:
        return color
    if colorType is list or colorType is bytearray:
        if type(color[0]) is float:
            color = [int(num * 255) for num in color]
        color = ['%.2x' % b for b in color]
        return "#{}{}{}".format(color[0], color[1], color[2])


# TODO simplify by not declaring/assigning segmentCenter, segmentLength, segmentDegrees
def createSegmentList(characterCenter):
    segmentList = []
    # segment 0
    segmentCenter = characterCenter + arr(
        [-(diagonalSpacing + halfShortSegmentLength), -(twiceDiagonalSpacing + shortSegmentLength)])
    segmentLength = shortSegmentLength
    segmentDegrees = 0
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 1
    segmentCenter = characterCenter + arr(
        [(diagonalSpacing + halfShortSegmentLength), -(twiceDiagonalSpacing + shortSegmentLength)])
    segmentLength = shortSegmentLength
    segmentDegrees = 0
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 2
    segmentCenter = characterCenter + arr(
        [- (twiceDiagonalSpacing + shortSegmentLength), -(diagonalSpacing + halfShortSegmentLength)])
    segmentLength = shortSegmentLength
    segmentDegrees = 90
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 3
    segmentCenter = characterCenter + arr(
        [-(diagonalSpacing + halfShortSegmentLength), -(diagonalSpacing + halfShortSegmentLength)])
    segmentLength = longSegmentLength
    segmentDegrees = 45
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 4
    segmentCenter = characterCenter + arr([0, -(diagonalSpacing + halfShortSegmentLength)])
    segmentLength = shortSegmentLength
    segmentDegrees = 90
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 5
    segmentCenter = characterCenter + arr(
        [diagonalSpacing + halfShortSegmentLength, -(diagonalSpacing + halfShortSegmentLength)])
    segmentLength = longSegmentLength
    segmentDegrees = -45
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 6
    segmentCenter = characterCenter + arr(
        [twiceDiagonalSpacing + shortSegmentLength, -(diagonalSpacing + halfShortSegmentLength)])
    segmentLength = shortSegmentLength
    segmentDegrees = 90
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 7
    segmentCenter = characterCenter + arr([-(diagonalSpacing + halfShortSegmentLength), 0])
    segmentLength = shortSegmentLength
    segmentDegrees = 0
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 8
    segmentCenter = characterCenter + arr([(diagonalSpacing + halfShortSegmentLength), 0])
    segmentLength = shortSegmentLength
    segmentDegrees = 0
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 9
    segmentCenter = characterCenter + arr(
        [- (twiceDiagonalSpacing + shortSegmentLength), (diagonalSpacing + halfShortSegmentLength)])
    segmentLength = shortSegmentLength
    segmentDegrees = 90
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 10
    segmentCenter = characterCenter + arr(
        [-(diagonalSpacing + halfShortSegmentLength), (diagonalSpacing + halfShortSegmentLength)])
    segmentLength = longSegmentLength
    segmentDegrees = -45
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 11
    segmentCenter = characterCenter + arr([0, (diagonalSpacing + halfShortSegmentLength)])
    segmentLength = shortSegmentLength
    segmentDegrees = 90
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 12
    segmentCenter = characterCenter + arr(
        [diagonalSpacing + halfShortSegmentLength, (diagonalSpacing + halfShortSegmentLength)])
    segmentLength = longSegmentLength
    segmentDegrees = 45
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 13
    segmentCenter = characterCenter + arr(
        [twiceDiagonalSpacing + shortSegmentLength, (diagonalSpacing + halfShortSegmentLength)])
    segmentLength = shortSegmentLength
    segmentDegrees = 90
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 14
    segmentCenter = characterCenter + arr(
        [-(diagonalSpacing + halfShortSegmentLength), twiceDiagonalSpacing + shortSegmentLength])
    segmentLength = shortSegmentLength
    segmentDegrees = 0
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    # segment 15
    segmentCenter = characterCenter + arr(
        [(diagonalSpacing + halfShortSegmentLength), twiceDiagonalSpacing + shortSegmentLength])
    segmentLength = shortSegmentLength
    segmentDegrees = 0
    segmentList.append(createSegmentPolygon(segmentCenter, segmentLength, segmentDegrees))
    return segmentList


def createSegmentPolygon(center, length, degrees):
    halfSegmentLength = length * 0.5
    radians = math.radians(degrees)
    xComponent = arr([math.cos(radians),math.sin(radians)])
    yComponent = arr([math.sin(radians),-math.cos(radians)])
    vertices = []
    # left point
    vertex = center - (xComponent * halfSegmentLength)
    vertices.append(vertex)
    # begin upper long side
    vertex = vertex + (xComponent * halfSegmentWidth) + (yComponent * halfSegmentWidth)
    vertices.append(vertex)
    # end upper long side
    vertex = vertex + (xComponent * (length - segmentWidth))
    vertices.append(vertex)
    # right point
    vertex = vertex + (xComponent * halfSegmentWidth) + (yComponent * -halfSegmentWidth)
    vertices.append(vertex)
    # begin lower long side
    vertex = vertex + (xComponent * -halfSegmentWidth) + (yComponent * -halfSegmentWidth)
    vertices.append(vertex)
    # end lower long side
    vertex = vertex + (xComponent * -(length - segmentWidth))
    vertices.append(vertex)
    return Polygon([Point(arr[0] * scale, arr[1] * scale) for arr in vertices])

class GraphicsCharacter(Character):
    def __init__(self, display, center):
        assert type(display) is GraphicsDisplay
        super().__init__(display)
        self.segments = createSegmentList(center)

    def setForeground(self, color):
        super().setForeground(normaliseColor(color))

    def drawSegment(self, index, color, show=True):
        color = normaliseColor(color)
        segment = self.segments[index]
        segment.undraw()
        segment.setFill(color)
        segment.draw(self.display.window)
        if show:
            self.show()

    def show(self):
        self.display.show()

class GraphicsDisplay(Display):
    def __init__(self, cols=None, rows=None, window=None, scale=None):
        super().__init__()
        if scale is not None:
            self.scale = scale
        else:
            self.scale = 0.036
        if window is not None:
            self.window = window
        else:
            windowWidth = self.scale * ((self.cols * characterDiameter) + ((self.cols + 1) * characterRadius))
            windowHeight = self.scale * ((self.rows * characterDiameter) + ((self.rows + 1) * characterRadius))
            self.window = GraphWin("Retrotextual", windowWidth, windowHeight, autoflush=False)
            self.window.setBackground("black")

        center = arr([characterDiameter,characterDiameter])
        for row in range(self.rows):
            for col in range(self.cols):
                self.characters.append(GraphicsCharacter(self, center))
                center[0] += characterDiameter + characterGap
            center[0] = characterDiameter
            center[1] = characterRadius * 5

    def show(self):
        self.window.update()
