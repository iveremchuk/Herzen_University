"""
Выполнил Веремчук Илья 3 курс ИВТ 1.1
"""
class FibonacciLst:
    def __init__(self):
        self.fibs_list = [0, 1]

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.fibs_list) < self.n:
            return self.fibs_list.pop()
        else:
            self.fibs_list.extend(self.fib(self.n - 1) + self.fib(self.n - 2))
            return self.fibs_list.pop()

    def __getitem__(self, index):
        if index >= 0:
            return self.fibs_list[index]
        else:
            raise IndexError("Index out of range")

    def fib(self, n):
        if n < 2:
            return n
        else:
            return self.fib(n - 1) + self.fib(n - 2)
