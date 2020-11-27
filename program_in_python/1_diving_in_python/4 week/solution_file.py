import os.path
import tempfile


class File:

    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            self.path = os.path.join(tempfile.gettempdir(), self.path)
            with open(self.path, 'tw', encoding='utf-8') as f:
                pass
        base = os.path.basename(self.path)
        self.name, self.ext = os.path.splitext(base)
        self.current = 0

    def __add__(self, obj):
        data = self.read() + obj.read()
        new_name = f'{self.name}+{obj.name}{self.ext}'
        new_file = File(new_name)
        new_file.write(data)
        return new_file

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path) as f:
            for index, line in enumerate(f):
                if index == self.current:
                    self.current += 1
                    return line
        raise StopIteration

    def __str__(self):
        return self.path

    def read(self):
        with open(self.path) as f:
            return f.read()

    def write(self, data):
        with open(self.path, 'w') as f:
            f.write(data)


def main():
    path_to_file = r'C:\Users\appol\PycharmProjects\module3\diving_in_python\4 week\1'
    storage_path = os.path.join(tempfile.gettempdir(), path_to_file)
    file_obj_1 = File(path_to_file + '_2' + '.txt')
    file_obj_3 = File(path_to_file + '_3' + '.txt')
    file_obj_1.write('line 1\n')
    file_obj_3.write('line 3\n')
    new_file_obj = file_obj_1 + file_obj_3
    for line in new_file_obj:
        print(ascii(line))


if __name__ == '__main__':
    main()
