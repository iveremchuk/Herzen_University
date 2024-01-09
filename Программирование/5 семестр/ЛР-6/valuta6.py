"""
Выполнил Веремчук Илья 3 курс ИВТ 1.1
"""
from urllib.request import urlopen  
from xml.etree import ElementTree as ET  
import time
from datetime import datetime

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()  
        return instances[cls]
    return getinstance

@singleton  
class CurrenciesList():
    def __init__(self):
        t = time.time()
        self._cur_time = datetime.fromtimestamp(t)
        self._last_call_time = t
        self._last_result = None

    @property
    def cur_time(self):
        return self._cur_time

    def get_currencies(self, currencies_ids_lst=None):
        t = time.time()
        if t - self._last_call_time < 1 and self._last_result is not None:
            return self._last_result
        self._last_call_time = t
        cur_res_str = urlopen("http://www.cbr.ru/scripts/XML_daily.asp")
        result = {}
        cur_res_xml = ET.parse(cur_res_str)  
        root = cur_res_xml.getroot()
        valutes = root.findall("Valute")
        for _v in valutes:
            valute_id = _v.get('ID')
            if str(valute_id) in currencies_ids_lst:
                valute_cur_val = _v.find('Value').text
                valute_cur_name = _v.find('Name').text
                result[valute_id] = (valute_cur_val, valute_cur_name)
        self._last_result = result
        return result
