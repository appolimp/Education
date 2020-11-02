import heapq

class Heap:
    def __init__(self):
        self.data = []

    @property
    def size(self):
        return len(self.data)

    @staticmethod
    def parent(i):
        return (i - 1) // 2

    def append(self, key):
        self.data.append(key)
        self.move_up(self.size - 1)

    def move_up(self, i):
        while i != 0 and self.data[self.parent(i)] > self.data[i]:
            self.data[self.parent(i)], self.data[i] = self.data[i], self.data[self.parent(i)]
            i = self.parent(i)

    def move_down(self, i):
        m, left, right = i, 2*i + 1, 2*i + 2
        if left < self.size and self.data[left] < self.data[m]:
            m = left
        if right < self.size and self.data[right] < self.data[m]:
            m = right
        if m == i:
            return

        self.data[i], self.data[m] = self.data[m], self.data[i]
        self.move_down(m)

    def change_priority(self, value, i=0):
        old_value = self.data[i]
        self.data[i] = value

        if old_value < value:
            self.move_down(i)
        else:
            self.move_up(i)

    def key_top(self):
        return self.data[0]

    def __str__(self):
        return ' '.join(str(i) for i in self.data)


class MyProc:
    def __init__(self, count):
        self.data = Heap()
        self.create_myproc(count)

    def create_myproc(self, count):
        for i in range(count):
            self.data.append((0, i))

    def __str__(self):
        return str(self.data)

    def take_task(self, dur):
        time, proc = self.data.key_top()
        print(proc, time)
        self.data.change_priority((time + dur, proc))


class HeapProc:
    def __init__(self, count):
        self.data = []
        for i in range(count):
            heapq.heappush(self.data, (0, i))

    def take_task(self, dur):
        time, proc = self.data[0]
        print(proc, time)
        heapq.heapreplace(self.data, (time + dur, proc))


def cool_heap(count, times):
    heap = [(0, i) for i in range(count)]
    for dur in times:
        time, proc = heap[0]
        print(proc, time)
        heapq.heapreplace(heap, (time + dur, proc))


if __name__ == '__main__':
    with open('1.txt') as f:
        reader = (tuple(map(int, line.split())) for line in f)
        n, _ = next(reader)
        times = next(reader)

    cool_heap(n, times)
    
    # process = MyProc(n)
    # process = HeapProc(n)
    # for t in times:
        # process.take_task(t)



