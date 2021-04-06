import yaml

yaml_level = """
!SomeGame
game: !game
    name: cool_game
    type: casual
    persons:
        - !pers
            name: Dmitriy
            age: 22
        - !pers
            name: Nikita
            age: 3
        - !pers
            name: Vova
            age: 23
"""


class FactoryGame(yaml.YAMLObject):

    @classmethod
    def from_yaml(cls, loader, node):

        def get_game(loader, node):
            data = loader.construct_mapping(node)
            game = cls.make_game(data['name'], data['type'])
            game.persons = data['persons']
            return game

        def get_per(loader, node):
            data = loader.construct_mapping(node)
            per = cls.make_per(**data)
            return per

        loader.add_constructor(u"!pers", get_per)
        loader.add_constructor(u"!game", get_game)

        return loader.construct_mapping(node)

    @classmethod
    def make_per(cls, name, age):
        return cls.Per(name, age)

    @classmethod
    def make_game(cls, name, type_):
        return cls.Game(name, type_)


class SomeGame(FactoryGame):
    yaml_tag = '!SomeGame'

    class Game:
        def __init__(self, name, type_):
            self.name = name
            self.type_ = type_

        def __str__(self):
            return f'{self.name} and {self.persons}'

    class Per:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def __repr__(self):
            return f'{self.name} from {self.age}'


if __name__ == '__main__':
    game = yaml.load(yaml_level, Loader=yaml.FullLoader)
    print(game['game'])