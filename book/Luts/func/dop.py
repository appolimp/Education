f1 = lambda a, b: print(a, b)
f2 = lambda a, *b: print(a, b)
f3 = lambda a, **b: print(a, b)
f4 = lambda a, *b, **c: print(a, b, c)
f5 = lambda a, b=2, c=3: print(a, b, c)
f6 = lambda a, b=2, *c: print(a, b, c)

f1(1, 2)
f1(b=2, a=1)

f2(1, 2, 3)
f3(1, x=2, y=3)
f4(1, 2, 3, x=2, y=3)

f5(1)
f5(1, 4)

f6(1)
f6(1, 3, 4)