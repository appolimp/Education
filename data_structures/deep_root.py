max_deep = 1
deep_dict = {}


def find_deep(i):
    if i not in deep_dict:
        if i == -1:
            deep_dict[i] = 1
        else:
            deep_dict[i] = 1 + find_deep(data[i])
    return deep_dict[i]


if __name__ == '__main__':
    text = '9 7 5 5 2 9 9 9 2 -1'
    data = [int(i) for i in text.split()]
    deep = 1
    for i in data:
        deep = max(deep, find_deep(i))

    print(deep)
