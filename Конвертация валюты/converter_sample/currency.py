from bs4 import BeautifulSoup
from decimal import Decimal
from requests.exceptions import HTTPError


class Currency:

    def __init__(self, bs4_struct):
        self.num_code = int(bs4_struct.find('numcode').text)
        self.char_code = bs4_struct.find('charcode').text
        self.nominal = int(bs4_struct.find('nominal').text)
        self.name = bs4_struct.find('name').text
        self.value = Decimal(bs4_struct.find('value').text.replace(',', '.'))

    def convert_by_amount(self, amount):
        result = Decimal(amount) / self.value * self.nominal
        return Decimal(result).quantize(Decimal("1.0000"))

    def convert_to(self, amount, currency):
        amount = Decimal(amount)
        result = self.convert_by_amount(amount) / currency.value * currency.nominal
        return Decimal(result).quantize(Decimal("1.0000"))


def convert(amount, cur_from, cur_to, date, requests):
    response = request_currency(requests=requests, date=date)
    if cur_from == "RUR" and cur_to == "RUR":
        return Decimal(amount).quantize(Decimal("1.0000"))
    elif cur_from == "RUR" or cur_to == "RUR":
        cur = cur_to if cur_from == "RUR" else cur_from
        currency = parse_currency(response=response, currency=cur)
        return currency.convert_by_amount(amount=amount)
    else:
        currency_from = parse_currency(response=response, currency=cur_from)
        currency_to = parse_currency(response=response, currency=cur_to)
        return currency_from.convert_to(amount=amount, currency=currency_to)


def request_currency(requests, date):
    try:
        endpoint = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
        req = requests.get(url=endpoint)
        req.raise_for_status()
        return req.text
    except HTTPError as http_error:
        print(f'HTTPError: {http_error}')
    except Exception as error:
        print(f'Exception: {error}')


def parse_currency(response, currency):
    bs = BeautifulSoup(markup=response, features="lxml")
    currency_to = bs.find(text=currency).parent.parent
    return Currency(bs4_struct=currency_to)
