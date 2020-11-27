import sys

digit_string = sys.argv[1]

print(sum(int(i) for i in digit_string))
