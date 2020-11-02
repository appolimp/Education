import time
import math


def timer(func, *args, n_iter=1_000_000):
    res = []
    for _ in range(n_iter):
        start = time.time()
        func(*args)
        res.append(time.time() - start)
    return sum(res)


def best(func, *args, n_iter=1000):
    bes = float('inf')
    for _ in range(n_iter):
        out = timer(func, *args, n_iter=1)
        bes = out if out < bes else bes
    return bes


print(timer(math.sqrt, 2**10), best(math.sqrt, 2**10))
print(timer(lambda x: x ** .5, 2**10), best(lambda x: x ** .5, 2**10))
print(timer(pow, 2**10, .5), best(pow, 2**10, .5))
