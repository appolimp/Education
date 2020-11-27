import os
from multiprocessing import Process
import time


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


class PrintProcess(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        info('info class f')
        print('hello', self.name)


if __name__ == '__main__':
    p = PrintProcess('Mike')
    p.start()
    p.join()
