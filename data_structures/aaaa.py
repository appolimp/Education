class Avl:
    def __init__(self):
        self.child = Knot()

    def min(self):
        return self.child.min()


class Knot:
    def __init__(self):
        self.value = 5

    def min(self):
        return self.value


cool = Avl()
print(cool.min())