from pprint import pprint
import json
from xml.etree import ElementTree


class ExportPet:
    def export(self, dog):
        raise NotImplementedError


class ExportJSON(ExportPet):
    def export(self, dog):
        return json.dumps({
            'name': dog.name,
            'breed': dog.breed,
        }, indent=4)


class ExportXML(ExportPet):
    def export(self, dog):
        return f"""<?xml version"1.0" encoding="utf-8"?>
<dog>
    <name>{dog.name}</name>
    <breed>{dog.breed}</breed>
</dog>"""


class Pet:
    def __init__(self, name):
        self.name = name


class Dog(Pet):
    def __init__(self, name, breed=None):
        super().__init__(name)
        self.breed = breed


class ExDog(Dog):
    def __init__(self, name, breed=None, exporter=None):
        super().__init__(name, breed)
        self._exporter = exporter or ExportJSON()
        if not isinstance(self._exporter, ExportPet):
            raise ValueError('bad exporter', exporter)

    def export(self):
        return self._exporter.export(self)


def main():
    dog = ExDog('aoao', 'Dvornaga')
    print(dog.export())
    pass


if __name__ == '__main__':
    main()
