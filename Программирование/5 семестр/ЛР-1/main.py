"""
Данная программа явлется Калькулятором.
На вход подают 2 числа и оператор действия над этими числами.
"""
import logging

def log_decorator(func):
    """
        Декоратор log_decorator, который принимает функцию func и возвращает новую функцию decorator. 
        Внутри decorator мы используем модуль logging для логирования информации о переданных аргументах и результате выполнения функции calculate. 
    """
    def decorator(num1, num2, operator):
        logging.info(f"Вызов функции calculate с аргументами: {num1}, {num2}, {operator}")
        result = func(num1, num2, operator)
        logging.info(f"Результат выполнения функции calculate: {result}")
        return result
    return decorator

@log_decorator
def calculate(num1, num2, operator, *args, tolerance=1e-6):
    """
        Функция calculate проверяет, какой оператор был введен, и выполняет соответствующее арифметическое действие
        num1 - первое число, которое вводит пользователь
        num2 - второе число, которое вводит пользователь
        operator - действие над этими числами
    """
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '**':
        result = num1 ** num2
    elif operator == '%':
        result = num1 % num2
    elif operator == '/':
        if num2 == 0:
            result = "Не делится на ноль"
        else:
            result = num1 / num2

    elif operator == 'medium':
            result = sum(args) / len(args)
        elif operator == 'variance':
            mean = sum(args) / len(args)
            result = sum((x - mean) ** 2 for x in args) / len(args)
        elif operator == 'std_deviation':
            mean = sum(args) / len(args)
            variance = sum((x - mean) ** 2 for x in args) / len(args)
            result = math.sqrt(variance)
        elif operator == 'median':
            sorted_args = sorted(args)
            n = len(args)
            if n % 2 == 0:
                result = (sorted_args[n // 2 - 1] + sorted_args[n // 2]) / 2
            else:
                result = sorted_args[n // 2] 
        elif operator == 'q3-q1':
            sorted_args = sorted(args)
            n = len(args)
            q1 = sorted_args[n // 4]
            q3 = sorted_args[(3 * n) // 4]
            result = q3 - q1
    else:
        result = "Некорректный оператор"
    
    precision = convert_precision(tolerance)
    return (result, precision)
    
def convert_precision(tolerance):
    return abs(int(calculate.log10(tolerance)))

def test_convert_precision():
    assert convert_precision(1e-6) == 6
    assert convert_precision(1e-3) == 3
    assert convert_precision(1e-10) == 10


def test_calculate():
    """
        Функция test_calculate() проверяет правильность работы функции calculate() с помощью нескольких тестовых случаев
    """
    assert calculate(4, 3, '+') == 7
    assert calculate(20, 17, '-') == 3
    assert calculate(6, 4, '*') == 24
    assert calculate(2, 3, '/') == 2/3
    assert calculate(100, 0, '/') == "Не делится на ноль"
    assert calculate(3, 3, '^') == "Некорректный оператор"
    assert calculate('medium', 1, 2, 3) == 2
    assert calculate('variance', 1, 2, 3) == 0.6666666666666666
    assert calculate('std_deviation', 1, 2, 3) == 0.816496580927726
    assert calculate('median', 1, 2, 3) == 2
    assert calculate('q3-q1', 1, 2, 3, 4, 5) == 3

def main():
    """
        Функция main() запрашивает у пользователя два числа и оператор, вызывает функцию calculate() и выводит результат
    """
    num1 = float(input("Введите первое число: "))
    num2 = float(input("Введите второе число: "))
    operator = input("Выберите оператор (+, -, *, /, **, %): ")
    result = calculate(num1, num2, operator)
    print("Результат: ", result)

if __name__ == '__main__':
    logging.basicConfig(filename='calculator.log', level=logging.INFO)
    main()
