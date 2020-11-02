# Загрузить стандартную библиотеку Python и библиотеку DesignScript
import sys
import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("DSCoreNodes")
import DSCore

clr.ImportExtensions(DSCore)
from DSCore import *


def create_countur(points):
    temp = []
    for x, y in points:
        temp.append(Point.ByCoordinates(float(x) / 1000, float(y) / 1000, 0))
    if len(temp) > 2:
        return Polygon.ByPoints(temp)

    return None


def main():
    data = IN[0]
    counturs = []
    error = []
    for layer, points in data:
        countur = create_countur(points)
        if countur:
            counturs.append([layer, countur])
        else:
            error = 5

    return counturs


print(main())
