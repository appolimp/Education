from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time

t = time.time()


def f(a):
    time.sleep(2)
    return f'{a * a}\t{time.time() - t:.5f}'


with ThreadPoolExecutor(max_workers=3) as pool:
    result = [pool.submit(f, i) for i in range(10)]

    for future in as_completed(result):
        print(future.result())

print(f'end\t{time.time()-t}')
