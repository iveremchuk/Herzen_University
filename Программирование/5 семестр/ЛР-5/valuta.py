import requests
from xml.etree import ElementTree as ET
import time

class CurrencyConverter:
    def __init__(self):
        self.currencies = []

    def get_currencies(self):
        cur_res_str = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(cur_res_str.content)
        valutes = root.findall("Valute")
        self.currencies = []
        for _v in valutes:
            valute_id = _v.get('ID')
            valute = {}
            valute_cur_name, valute_cur_val = _v.find('Name').text, _v.find('Value').text
            valute_charcode = _v.find('CharCode').text
            valute[valute_charcode] = (valute_cur_name, valute_cur_val)
            self.currencies.append(valute)
        self.timestamp = time.time()

    def get_currency_value(self, currency_id):
        for currency in self.currencies:
            if currency_id in currency:
                return currency[currency_id]

    def add_currency(self, currency_id, currency_name, currency_value):
        self.currencies.append({currency_id: (currency_name, currency_value)})

    def __del__(self):
        print("CurrencyConverter object deleted")

# Пример
converter = CurrencyConverter()
converter.get_currencies()
print(converter.currencies)
print(converter.get_currency_value('USD'))
converter.add_currency('TEST', 'Test Currency', '1.0')
print(converter.currencies)

# Тесты
converter = CurrencyConverter()
converter.get_currencies()
print(converter.get_currency_value('R9999'))  # {'R9999': None}
print(converter.get_currency_value('USD'))  # Test with a valid currency ID
