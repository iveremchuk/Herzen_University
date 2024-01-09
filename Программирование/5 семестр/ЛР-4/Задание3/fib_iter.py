"""
Выполнил Веремчук Илья 3 курс ИВТ 1.1
"""
from itertools import islice

def fib_iter(iterable):
    a, b = 0, 1
    for _ in range(2, len(iterable)):
        a, b = b, a + b
        yield a

l = list(range(14))
print(list(islice(fib_iter(l), 0, 2))) 
