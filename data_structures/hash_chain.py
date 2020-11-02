class HashChain:
    def __init__(self, m):
        self.data = [[] for _ in range(m)]

    def add(self, string):
        i = self.hash_string(string)
        if self._find(string, i):
            return

        self.data[i].insert(0, string)

    def check(self, num):
        print(*self.data[int(num)] or '')

    def delete(self, string):
        i = self.hash_string(string)
        if not self._find(string, i):
            return

        self.data[i].remove(string)

    def _find(self, string, i=None):
        i = i or self.hash_string(string)
        return True if string in self.data[i] else False

    def find(self, string):
        if self._find(string):
            print('yes')
        else:
            print('no')

    def hash_string(self, string):
        p, x = 1_000_000_007, 263
        i = 0
        _sum = 0

        for ch in string:
            num = ord(ch) * (x ** i)
            _sum = (_sum + num) % p
            i += 1

        return _sum % len(self.data)


if __name__ == '__main__':
    with open('1.txt') as f:
        m = int(f.readline())
        _ = f.readline()
        book = HashChain(m)

        reader = (line.split() for line in f)
        for com, world in reader:
            if com == 'del':
                com = 'delete'

            getattr(book, com)(world)
