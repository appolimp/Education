import sys


def in_order(data, key):
	if key != -1:
		yield from in_order(data, data[key][1])
		yield data[key][0]
		yield from in_order(data, data[key][2])


def pre_order(data, key):
	if key != -1:
		yield data[key][0]
		yield from pre_order(data, data[key][1])
		yield from pre_order(data, data[key][2])


def post_order(data, key):
	if key != -1:
		yield from post_order(data, data[key][1])
		yield from post_order(data, data[key][2])
		yield data[key][0]


def main():
	# with sys.stdin as f:
	with open('1.txt') as f:
		reader = (tuple(map(int, line.split())) for line in f)
		next(reader)
		data = [val for val in reader]

	print(*in_order(data, 0))
	print(*pre_order(data, 0))
	print(*post_order(data, 0))


if __name__ == '__main__':
	main()
