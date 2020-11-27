from pprint import pprint


class FileReader:

    def __init__(self, path):
        self.path = path

    def read(self):
        try:
            with open(self.path) as f:
                return f.read()
        except FileNotFoundError:
            return ''


def main():
    reader = FileReader('not_found.txt')
    text = reader.read()
    pprint(text)

    with open('1.txt', 'w') as file:
        file.write('some text')

    reader = FileReader('1.txt')
    text = reader.read()
    pprint(text)
    print(type(reader))


if __name__ == '__main__':
    main()