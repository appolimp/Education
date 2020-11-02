from threading import Thread, RLock
import time
from queue import Queue


class Point(object):
    def __init__(self):
        self._muter = RLock()
        self._x = 0
        self._y = 0

    def get(self):
        with self._muter:
            return self._x, self._y

    def set(self, x, y):
        with self._muter:
            self._x = x
            self._y = y


def worker(q, n):

    while True:
        p = Point()
        t = q.get()
        if t is None:
            break
        p.set(n, n*10+t)
        time.sleep(1)
        print(f'point: {p.get()}')


def main():
    q = Queue(5)
    th1 = Thread(target=worker, args=(q, 1))
    th2 = Thread(target=worker, args=(q, 2))
    th1.start(); th2.start()
    for i in range(10):
        q.put(i)

    q.put(None)
    q.put(None)

    th1.join()
    th2.join()


if __name__ == '__main__':
    main()
