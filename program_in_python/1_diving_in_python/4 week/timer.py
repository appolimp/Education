import time


class timer:
    def __init__(self):
        self.start = time.time()

    def current_time(self):
        print(f'Elapsed: {(time.time() - self.start) * 1000:.3f} мс')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.current_time()


with timer() as t:
    time.sleep(1)
    t.current_time()
    time.sleep(1)