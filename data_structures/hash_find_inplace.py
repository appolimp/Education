import random


class HashInPlace:
    def __init__(self, pattern):
        self.p = 1_000_000_007
        self.x = random.randint(1, self.p-1)
        self.x = 298_625_651

        self.data = ''
        self.pattern = pattern
        self.pow_x = self.create_pow_x()

    def mod_p(self, value):
        return (value % self.p + self.p) % self.p

    def create_pow_x(self):
        pow_x = [1]
        x = self.x
        for i in range(1, len(self.pattern)):
            pow_x.append(self.mod_p(pow_x[-1] * x))
        return pow_x

    def h_inplace(self, hash_, ch):
        ...

    def get_hash(self, string):
        p, x = self.p, self.x
        _sum = 0
        for i, ch in enumerate(string):
            num = self.mod_p(ord(ch) * self.pow_x[len(self.pattern)-i-1])
            _sum = self.mod_p(_sum + num)
        return _sum

    def can_take(self, ch):
        if len(self.data) >= len(pattern):
            return False

        self.data += ch
        if len(self.data) == len(pattern):
            self.h_pattern = self.get_hash(pattern)
            self.h_temp = self.get_hash(self.data)
        return len(self.data) <= len(pattern)


if __name__ == '__main__':
    with open('1.txt') as f:
        pattern = f.readline().strip()
        text = f.readline().strip()

    hash_ = HashInPlace(pattern)

    gen = (i for i in text)
    for i in range(len(pattern)):
        hash_.data += next(gen)

    hash_.h_pattern = hash_.get_hash(pattern)
    hash_.h_temp = hash_.get_hash(hash_.data)

    print(hash_.data)
    print(hash_.h_pattern, hash_.h_temp)