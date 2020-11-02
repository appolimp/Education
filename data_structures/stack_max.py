from collections import deque


class Stack:
    def __init__(self):
        self.__data = []

    def push(self, key):
        temp_max = self.__data[-1][-1] if self.__data else key
        self.__data.append((key, max(temp_max, key)))

    def pop(self, *args):
        return self.__data.pop()

    def max(self, *args):
        return self.__data[-1][-1]


if __name__ == '__main__':
    import sys
    # with sys.stdin as f:
    with open('1.txt') as f:
        n = f.readline()

        reader = (line.split() for line in f)
        buffer = Stack()
        for com, *num in reader:
            getattr(buffer, com)(num)



