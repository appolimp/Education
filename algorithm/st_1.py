d = dict(zip(input(), input()))
d0 = dict(zip(d.values(), d.keys()))
print(d0)
print(input().translate(d))
print(input().translate(d0))