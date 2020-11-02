import queue

"""
def min_stack(cls):
    callable_attributes = {k: v for k, v in cls.__dict__.items()
                           if callable(v)}
    for name, func in callable_attributes.items():
        decorated = ...(func)
        setattr(cls, name, decorated)

    return cls
"""


class Stack:
    def __init__(self):
        self.data = []
        self.min_data = []

    def put(self, key):
        self.data.append(key)
        self.min_data.append(key if key > self.key_min() else self.key_min())

    def key_top(self):
        return self.data[-1]

    def get(self):
        self.min_data.pop()
        return self.data.pop()

    def get_min(self):
        self.data.pop()
        return self.min_data.pop()

    def key_min(self):
        if self.min_data:
            return self.min_data[-1]
        return float('-inf')

    def empty(self):
        return not self.data

    def __iter__(self):
        return self

    def __next__(self):
        if self:
            return self.get()
        raise StopIteration

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return ' '.join(str(i) for i in self.data)

    def __bool__(self):
        return not self.empty()


class DoubleStack:
    def __init__(self, size):
        self.left = Stack()
        self.right = Stack()
        self.size = size

    def put(self, key):
        if len(self.left) == self.size and self.right.empty():
            for el in self.left:
                self.right.put(el)
        self.left.put(key)
        print(self.left, '~', self.right, '~\t', self.key_min(), '~\t', self.left.min_data, '~', self.right.min_data)

    def get(self):
        if self.right:
            return self.right.get()

    def get_min(self):
        right = self.right.get_min() if self.right else float('-inf')
        left = self.left.key_min() if self.left else float('-inf')
        # left = self.left.get_min() if self.size == len(self.left) else float('-inf')
        return max(right, left)

    def key_min(self):
        right = self.right.key_min() if self.right else float('inf')
        left = self.left.key_min() if self.left else float('inf')
        return max(right, left)

    def __len__(self):
        return len(self.right) + len(self.left)


def is_correct_brace(data):
    brace = {'[': ']',
             '{': '}',
             '(': ')'}
    s = Stack()
    for ch in data:
        if ch in brace:
            s.put(brace[ch])
        elif ch in brace.values():
            if s.empty():
                return False
            if ch != s.get():
                return False

    return s.empty()


def find_number(data, m):
    res = []
    stack = DoubleStack(m)

    for num in data:
        if len(stack) < m-1:
            stack.put(num)
            continue

        stack.put(num)
        res.append(stack.get_min())

    return res


if __name__ == '__main__':
    """
    text = '([ghj{[([ghjfjghj])fgfghjj]}fghj])'
    print(is_correct_brace(text))
    """

    n = 8
    A = [int(i) for i in '2 7 3 1 5 2 6 2'.split()]
    m = int(4)

    print(find_number(A, m))

