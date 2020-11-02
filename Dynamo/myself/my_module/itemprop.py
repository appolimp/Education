class Polygon:
    def __init__(self, layer=None, points=None, color=(255, 255, 255)):
        self.points = points
        self.layer = layer
        self.prop = set()
        self.color = color

    def set_point(self, points):
        self.points = points

    def set_layer(self, layer):
        self.layer = layer

    def set_prop(self, prop):
        """

        :type prop: object
        """
        self.prop = prop

    def set_color(self, color):
        """

        :type color: object
        """
        self.color = color
