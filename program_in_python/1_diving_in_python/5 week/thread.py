from threading import Thread
import os


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def f(name):
    info('info class f')
    print(f'Hello, {name}!')


print(os.getpid())
th = Thread(target=f, args=('Bob',))
th.start()
th.join()