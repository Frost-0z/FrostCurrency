import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(base: str, symbols: str, amount: str):
        if base == symbols:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            symbols_ticker = keys[symbols]
        except KeyError:
            raise ConvertionException(f'Не удалось распознать валюту {symbols}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось распознать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        url = f'https://api.apilayer.com/fixer/latest?symbols={symbols_ticker}&base={base_ticker}'

        headers = {
            'apikey': '4K8F4M5TSEMrNRuPdbiYATX9K7ijbBCa'
        }
        response = requests.get(url, headers=headers)
        result = response.text
        total_result = json.loads(result)['rates'].get(symbols_ticker)

        return total_result