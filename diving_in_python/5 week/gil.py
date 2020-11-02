from threading import Thread
import time


def count(n):
    while n > 0:
        n -= 1
        # time.sleep(0.018699)


# series_run
t0 = time.time()
count(100_000_000)
count(100_000_000)
print(f'series = {time.time() - t0:.3f}')

# parallel run
t0 = time.time()
th1 = Thread(target=count, args=(100_000_000,))
th2 = Thread(target=count, args=(100_000_000,))

th1.start()
th2.start()

th1.join()
th2.join()
print(f'parallel = {time.time() - t0:.3f}')
