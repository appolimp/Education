import math
from abc import ABC, abstractmethod


class Base(ABC):
    def __init__(self, data, result):
        self.data = data
        self.result = result

    @property
    def ans(self):
        return [int(x >= 0.5) for x in self.data]

    @abstractmethod
    def get_loss(self):
        pass

    def get_score(self):
        return sum([int(x == y) for (x, y) in zip(self.ans, self.result)]) \
            / len(self.ans)


class A(Base):
    def get_loss(self):
        return sum([(x - y) * (x - y) for (x, y) in zip(self.data, self.result)])


class B(Base):
    def get_loss(self):
        return -sum([
            y * math.log(x) + (1 - y) * math.log(1 - x)
            for (x, y) in zip(self.data, self.result)
        ])

    def get_score(self):
        res = [int(x == 1 and y == 1) for (x, y) in zip(self.ans, self.result)]
        pre = sum(res) / sum(self.ans)
        rec = sum(res) / sum(self.result)
        return 2 * pre * rec / (pre + rec)


class C(Base):
    def get_loss(self):
        return sum([abs(x - y) for (x, y) in zip(self.data, self.result)])