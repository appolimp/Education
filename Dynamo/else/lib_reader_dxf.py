import ezdxf
from pprint import pprint
doc = ezdxf.readfile('Пример_1.dxf')
msp = doc.modelspace()

points = []

for line in msp.query('LWPOLYLINE'):
    layer = line.dxf.layer
    point = [i[:2] for i in line]
    points.append([layer, point])
print(*points, sep='\n')
print(len(points))