import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def parse_currency():
    URL = 'https://coinmarketcap.com/ru/currencies/toncoin/'

    r = requests.get(URL)
    soup = bs(r.text, 'html.parser')
    html_currency_ton = soup.find_all('div', class_='priceValue')
    split_currency = str(html_currency_ton[0]).split('>')
    end_currency_ton = split_currency[2].split('<')[0]

    return end_currency_ton
