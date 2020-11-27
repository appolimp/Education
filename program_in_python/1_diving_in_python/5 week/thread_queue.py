# from queue import Queue
from threading import Thread, RLock, Condition
import time


class Queue:
    def __init__(self, size=5):
        self._size = size
        self._queue = []
        self._mutex = RLock()
        self._empty = Condition(self._mutex)
        self._full = Condition(self._mutex)

    def put(self, val):
        with self._full:
            while len(self._queue) >= self._size:
                self._full.wait()

            self._queue.append(val)
            self._empty.notify()

    def get(self):
        with self._empty:
            while len(self._queue) == 0:
                self._empty.wait()

            ret = self._queue.pop(0)
            self._full.notify()
            return ret

    def __repr__(self):
        return ' '.join(str(i) for i in self._queue)


def worker(q, n):
    while True:
        item = q.get()
        if item is None:
            break
        print(((n, '~', q), ("process data:", n, item)))
        time.sleep(1)


q = Queue(5)
th1 = Thread(target=worker, args=(q, 1))
th2 = Thread(target=worker, args=(q, 2))
th1.start()
th2.start()

for i in range(20):
    q.put(i)

q.put(None)
q.put(None)
th1.join()
th2.join()
