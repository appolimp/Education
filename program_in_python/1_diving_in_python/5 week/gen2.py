def chain(x_it, y_it):
    yield from x_it
    yield from y_it


def the_same(x_it, y_it):
    for x in x_it:
        yield x

    for y in y_it:
        yield y


a = [1, 2, 3]
b = (4, 5)

for x in chain(a, b):
    print(x)
