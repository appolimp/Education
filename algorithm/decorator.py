
def new_decorator(b=10):

    def decorator(func):

        def innit(a):
            a += b
            return func(a)

        return innit

    return decorator


@new_decorator(50)
def number(a):
    return a


print(number(5))
'''
new_number = decorator(number, 10)
print(new_number(5))
'''