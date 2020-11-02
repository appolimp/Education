import ezdxf
from color_rgb import color_base
from itemprop import Polygon


class FindDxf:
    def __init__(self, path):
        self.path = path
        self.__doc = ezdxf.readfile(self.path)
        self.__msp = self.__doc.modelspace()

    def find(self, req):
        __data = []
        for line in self.__msp.query(req):
            layer = line.dxf.layer
            color = self.get_color_layer(layer)
            points = self.correct_point(line)
            __data.append(Polygon(layer, points, color))
        return __data

    @staticmethod
    def correct_point(line):
        return [tuple(round(x) for x in point[:2]) for point in line]

    def get_color_layer(self, name):
        layer = self.__doc.layers.get(name)
        anc = layer.dxf.color
        return color_base[str(anc)]


if __name__ == '__main__':
    file = FindDxf('primer.dxf')
    data_poly = file.find('LWPOLYLINE')