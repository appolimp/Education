import sys

a = int(sys.argv[1])
b = int(sys.argv[2]) 
c = int(sys.argv[3])

D = (b ** 2 - 4 * a * c) ** 0.5
for d in (D, -D):
    print(int((-b + d) / (2 * a)))
