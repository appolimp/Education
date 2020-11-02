import random


class HashText:
    def __init__(self, pattern, text):
        self.pattern = pattern
        self.text = text
        self.dict_x = {0: 1}
        self.p = 1_000_000_007
        self.x = random.randint(1, self.p-1)
        self.h_pattern = self.get_hash(pattern)
        self.h_text = []

    def mod_p(self, value):
        return (value % self.p + self.p) % self.p

    def get_hash(self, string):
        p, x = self.p, self.x
        _sum = 0

        for i, ch in enumerate(string):
            if i not in self.dict_x:
                self.dict_x[i] = self.mod_p(self.dict_x[i-1] * x)
            num = ord(ch) * self.dict_x[i]
            _sum = ((_sum + num) % p + p) % p

        return _sum

    def create_h_text(self):
        self.h_text = [0 for _ in range(len(self.text) - len(pattern) + 1)]

    def create_last_h(self):
        i = len(self.h_text) - 1
        # print(self.text[i:], self.get_hash(self.text[i:]))
        # print(self.pattern, self.get_hash(self.pattern))
        self.h_text[i] = self.get_hash(self.text[i:])

    def calc_h(self, i):
        len_p = len(self.pattern)
        x_i = self.dict_x[len_p - 1]

        _diff = self.mod_p(self.h_text[i-1] - ord(self.text[i-1]) * x_i)

        self.h_text.append(self.mod_p(_diff * self.x + ord(self.text[i+len_p-1])))
        return self.h_text[i]


if __name__ == '__main__':
    with open('1.txt') as f:
        pattern = f.readline().strip()
        text = f.readline().strip()

    hash_text = HashText(pattern, text)
    hash_text.h_text = [hash_text.get_hash(text[:len(pattern)])]

    for i in range(1, len(text) - len(pattern) + 1):
        hash_text.calc_h(i)

    for i, h_t in enumerate(hash_text.h_text):
        if h_t == hash_text.h_pattern:
            if text[i:i+len(pattern)] == pattern:
                print(i, text[i:i+len(pattern)])

    print(hash_text.h_text)
    print(hash_text.h_pattern)
