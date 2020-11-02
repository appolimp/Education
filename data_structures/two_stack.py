from collections import deque


class DoubleStack:
    def __init__(self, size):
        self._size = size
        self.left = deque()
        self.right = deque()

    def add_num(self, num):
        if len(self.left) == self._size:
            for _ in range(len(self.left)):
                prev = self.left.pop()
                temp_max = self.right[-1] if self.right else prev
                self.right.append(max(prev, temp_max))

        temp_max = self.left[-1] if self.left else num
        self.left.append(max(num, temp_max))

    def get_max(self):

        max_left = self.left[-1] if self.left else float('-inf')
        max_right = self.right.pop() if self.right else float('-inf')

        return max(max_left, max_right)


if __name__ == '__main__':
    import sys
    # with sys.stdin as f:
    with open('1.txt') as f:
        _ = f.readline()

        data = (tuple(int(i) for i in f.readline().split()))
        size = int(f.readline())

        buffer = DoubleStack(size)
        data_max = []

        for num in data:
            buffer.add_num(num)
            data_max.append(buffer.get_max())

    print(*data_max[size-1:])

