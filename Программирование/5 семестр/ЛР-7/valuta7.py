"""
Выполнил Веремчук Илья 3 курс ИВТ 1.1
"""
from abc import ABC, abstractmethod
import requests
import json
import csv

class CurrenciesList(ABC):
    @abstractmethod
    def get_currencies(self) -> dict:
        pass

class BasicCurrenciesList(CurrenciesList):
    def get_currencies(self) -> dict:
        pass

class CurrencyDecorator(CurrenciesList):
    def __init__(self, currency_list: CurrenciesList):
        self._currency_list = currency_list

    def get_currencies(self) -> dict:
        return self._currency_list.get_currencies()

class ConcreteDecoratorJSON(CurrencyDecorator):
    def get_currencies(self) -> dict:
        data = self._currency_list.get_currencies()
        return json.dumps(data)

class ConcreteDecoratorCSV(CurrencyDecorator):
    def get_currencies(self) -> str:
        data = self._currency_list.get_currencies()
        

# Пример 
basic = BasicCurrenciesList()
decorated = ConcreteDecoratorJSON(basic)
result = decorated.get_currencies()
print(result)
