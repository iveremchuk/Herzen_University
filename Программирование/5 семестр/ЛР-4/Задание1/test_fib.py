def fib(n):
    fib_list = [0, 1]
    while fib_list[-1] <= n:
        fib_list.append(fib_list[-1] + fib_list[-2])
    return fib_list[:-1]
