import json


def to_json(func):
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, set):
            result = list(result)
        return json.dumps(result, sort_keys=True)

    return wrapped


@to_json
def get_data():
    return {'data': 42}


@to_json
def get_int():
    return 2


@to_json
def get_set():
    set_ret = set()
    set_ret.add(42)
    return set_ret


@to_json
def get_list():
    return [2]


@to_json
def get_tuple():
    return tuple(('python', 'json', 'mysql'))


@to_json
def get_str():
    return 'test'


@to_json
def get_float():
    return 3.4


@to_json
def get_bool():
    return True


@to_json
def get_none():
    return None


@to_json
def get_lol():
    return '""'


@to_json
def f(a, b, c):
    return [a, b, c]


print(get_data())  # вернёт '{"data": 42}'
print(get_int())
print(get_set())
print(get_list())
print(get_tuple())
print(get_str())
print(get_float())
print(get_bool())
print(get_none())
print(get_lol())
print(f(1, 2, 3))  # '[1, 2, 3]'

