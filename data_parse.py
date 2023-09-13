import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv
import re

url = 'https://www.585zolotoy.ru/catalog/gold-bracelets-with-stones/'
headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'connection': 'keep-alive',
        'cookie': 'auth.strategy=local; zolotoy_region=a93acc32-8ed4-48ed-b105-abd0eb856021; cart=%5B%5D; _userGUID=0:lmgve9de:LHIQ1Cl3dUTiPPvw8fn~p5DZyUDJz~zC; _gid=GA1.2.921373496.1694556850; _ym_uid=1694556850352480640; _ym_d=1694556850; _ym_isad=2; tmr_lvid=572988e63bc9ee4f98830ae339533c2a; tmr_lvidTS=1694556850658; app-popup-shown=1; top-line-banner.3bc40d14e6d9d0e0bfa1d738=1; top-line-banner=1; _ga_750VBXG7ZL=GS1.1.1694597046.4.1.1694612125.0.0.0; _ga=GA1.2.433828691.1694556849; _ga_1RZK4JTBYW=GS1.2.1694597048.4.1.1694612125.46.0.0; tmr_detect=0%7C1694612128511; qrator_jsr=1694614451.727.kM1dIGxyge0afGO3-5pp9otmg5e7sb31ijgk59m1sufuticpq-00; qrator_jsid=1694614451.727.kM1dIGxyge0afGO3-jj2c414ge7gknph7rqmbmdrc161h78b1; qrator_ssid=1694614452.404.OdLC4WeUXw6P1qhd-ot24labmgkhmii1oa2sp40oepqjmfi5o',
        'host': 'www.585zolotoy.ru',
        'If-None-Match': "d36d3-C+r81N2cAVTK9QN/6xveZyR7v1w",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows"}

r = requests.get(url, headers=headers)
print(r.status_code)

'''Парсинг названий элементов'''

soup = bs(r.text, 'lxml')
products = soup.find('ul', class_='tiles')
all_products = ''

for n, i in enumerate(products, start=1):
    try:
        product = i.find('div', class_='product-name caption-1 info has-old-price').find('a').text.strip()
    except:
        product = i.find('div', class_='product-name caption-1 info').find('a').text.strip()
    all_products += product + ';'

all_products = all_products.split(';')
print(all_products)
def my_func(name):
    with open(name, 'r', encoding= 'utf-8') as file:
        string = file.readlines()
        string = string[0].split('\n')
        # print(string)
        file.close()
    return string

'''Парсинг цен''' 

prices = soup.find_all('div', class_='price-row')
all_prices = ''

for n, i in enumerate(prices, start=1):
    itemPrice1 = i.find('div', class_='title-4 semi info m2 actual-price-row').find('span').text.strip()
    # print(itemPrice1)
    all_prices += 'Актуальная цена: ' + itemPrice1
    try:
        itemPrice2 = i.find('div', class_='flex old-price-row info').find('span', class_='body-2 c-text-secondary strike').text.strip()
        # print(itemPrice2)
        all_prices += 'Старая цена: ' + itemPrice2 
    except:
        pass
    all_prices += ';'

new_price = ''

def make_list():
    symbols = 'СтараяАктуальнаяцена :1234567890₽о;'
    x = ''
    for s in all_prices:
        if s in symbols:
            if s == '₽':
                x += s + ' '
            else:
                x += s
    return x

sc = ' Старая цена: ' + str(0) + '₽ '

all_prices = make_list()
all_prices = all_prices.split(';')
all_prices_changed = []

for i in all_prices:
    if len(i) < 30:
        all_prices_changed.append(i + sc)
    else:
        all_prices_changed.append(i)

print(all_prices_changed)      

nums = re.findall(r'\d+', str(all_prices_changed))
nums = [int(i) for i in nums]

np = []
op = []
q = 0
for i in nums:
    if q % 2 == 0:
        if q == 49:
            pass
        else:
            np.append(i)
            q += 1
    else:
        op.append(i)
        q += 1
print(op)
print(np)
'''Парсинг ссылок'''

links = soup.find_all('li', class_='product-tile type-default')
all_links = ''

for n, i in enumerate(links, start=1):
    try:
        link1 = i.find('div', class_='product-name caption-1 info has-old-price').find('a')['href']
    except:
        link1 = i.find('div', class_='product-name caption-1 info').find('a')['href']
    if link1 is None:
        pass
    else:
        all_links += link1 + ';'

all_links = all_links.split(';')
# print(all_links)

print(len(all_links), len(op), len(np), len(all_products))

with open("testovoe.csv", mode="w", encoding='utf-8') as file:
    file_writer = csv.writer(file, delimiter = ",", lineterminator="\n")
    file_writer.writerow(['Имена', 'Цена старая', 'Цена новая', 'Ссылки'])
    for i in range(0, len(all_links)):
        try:
            row = [all_products[i], op[i], np[i], all_links[i]]
        except: 
            pass
        file_writer.writerow(row)