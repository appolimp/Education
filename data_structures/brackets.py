from collections import deque


def check_brackets(text):
    brackets = {'[': ']',
                '{': '}',
                '(': ')'}

    deq = deque()
    for i, ch in enumerate(text, start=1):
        if ch in brackets:
            deq.append((brackets[ch], i))
        elif ch in brackets.values():
            if not deq or ch != deq.pop()[0]:
                return i

    return deq.popleft()[1] if deq else 'Success'


if __name__ == '__main__':
    print(check_brackets('[]'))
    assert check_brackets('[]') == 'Success'
    assert check_brackets('{}[]') == 'Success'
    assert check_brackets('[()]') == 'Success'
    assert check_brackets('(())') == 'Success'
    assert check_brackets('{[]}()') == 'Success'
    assert check_brackets('{') == 1
    assert check_brackets('{[}') == 3
    assert check_brackets('foo(bar);') == 'Success'
    assert check_brackets('foo(bar[i);') == 10


