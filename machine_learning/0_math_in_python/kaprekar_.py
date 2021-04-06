

def kaprekar(n):
    def get_num(list_num):
        num = int(''.join(list_num))
        return num if num else float('-inf')

    k = str(n ** 2)
    c = [get_num(k[:i]) + get_num(k[i:]) == n for i in range(1, len(k))]
    return any(c)


print(kaprekar(100))
