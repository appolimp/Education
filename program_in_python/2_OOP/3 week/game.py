from pprint import pprint


class Light:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(3)] for _ in range(3)]
        self.map[2][2] = 1  # Источники света
        self.map[1][1] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee((0, 0))

    def lighten(self, grid):
        width = len(grid)
        height = len(grid[0])
        self.adaptee.set_dim((width, height))
        for w in range(width):
            for h in range(height):
                if grid[w][h] == 1:
                    self.adaptee.set_lights((w, h))
                elif grid[w][h] == -1:
                    self.adaptee.set_obstacles((w, h))

        return self.adaptee.generate_lights()


if __name__ == '__main__':
    system = System()
    light_mapper = MappingAdapter(Light)

    system.get_lightening(light_mapper)
    print(*system.lightmap, sep='\n')
