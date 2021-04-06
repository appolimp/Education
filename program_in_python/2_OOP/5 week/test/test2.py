import yaml

yaml_text = """
levels:
  - !random_map
        rat: 12
        done: 23
  - !end_map {}
"""


class FabricLevel(yaml.YAMLObject):

    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_mapping(node)
        print(data)
        return {'map': cls.Map(), 'obj': cls.Objects()}


class EndMap(FabricLevel):
    yaml_tag = "!end_map"

    class Map:
        def __init__(self):
            self.Map = ['000000000000000000000000000000000000000',
                        '0                                     0',
                        '0                                     0',
                        '0  0   0   000   0   0  00000  0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  000    0   0  00000  0000   0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  0   0   000   0   0  00000  00000  0',
                        '0                                   0 0',
                        '0                                     0',
                        '000000000000000000000000000000000000000'
                        ]
            self.Map = list(map(list, self.Map))

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            return self.objects


class RandomMap(FabricLevel):
    yaml_tag = "!random_map"

    class Map:

        def __init__(self):
            self.Map = [[0 for _ in range(41)] for _ in range(41)]

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            return self.objects


level_list = yaml.load(yaml_text, Loader=yaml.FullLoader)['levels']
level_list.append({'map': EndMap.Map(), 'obj': EndMap.Objects()})

print(*level_list, sep='\n')
