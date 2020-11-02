def adder(**kwargs):
    return sum(kwargs.values())


def copy_dict(dict: dict):
    from copy import deepcopy
    return deepcopy(dict)


def add_dict(dict1: dict, dict2: dict) -> dict:
    if type(dict1) == list:
        return dict1 + dict2
    new_dict = copy_dict(dict1)
    a['b'][0] = 12
    new_dict.update(dict2)
    return new_dict


a = {'a': 123, 'b': [1, 2, 3]}
b = {'a': 456, 'c': [1, 2, 3]}


print(add_dict(a, b))
print(a)
print(b)

print(add_dict([1, 2, 3], [4, 5, 6]))

"""
print(adder(1, 3, 5))
print(adder('11', '22', '33'))
print(adder([1, 2, 3], [4, 5, 6], [7, 8, 9]))
"""
