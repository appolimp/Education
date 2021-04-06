import yaml

yaml_file = """
--- !Game1
objects:
    - some_text: ...
game: !game
    name: !!str 'Cool Game'
    persons:
        - !person
            name: !!str mage
            weight: !!float 5
        - !person
            name: !!str warrior
            weight: !!float 10
        - !person
            name: !!str assassin
            weight: !!float 0
        
"""


class GameFactory(yaml.YAMLObject):

    @classmethod
    def from_yaml(cls, loader, node):

        def get_game(loader, node):
            data = loader.construct_mapping(node)
            my_game = cls.make_game(data['name'])
            my_game.persons = data["persons"]
            return my_game

        def get_person(loader, node):
            data = loader.construct_mapping(node)
            per = cls.make_person(**data)
            return per

        loader.add_constructor('!game', get_game)
        loader.add_constructor('!person', get_person)

        return loader.construct_mapping(node)['game']

    @classmethod
    def make_game(cls, name):
        return cls.Game(name)

    @classmethod
    def make_person(cls, name, weight):
        return cls.Person(name, weight)


class CoolGame(GameFactory):
    yaml_tag = '!Game1'

    class Game:
        def __init__(self, name):
            self.name = name
            self.persons = []

        def __str__(self):
            return "Game {} with: {}".format(self.name, '\n\t\t\t\t\t '.join(str(i) for i in self.persons))

    class Person:
        def __init__(self, name, weight):
            self.name = name
            self.weight = weight

        def __repr__(self):
            return f'{self.name} as {self.weight}'

        def __str__(self):
            return f'{self.name} as {self.weight}'


game = yaml.load(yaml_file, Loader=yaml.FullLoader)
print(game)