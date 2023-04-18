import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST = 'https://sokolov.ru/'
URL = 'https://sokolov.ru/watch-catalog/watches/men/?stock=Y'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sklv-product__inner')
    cards = []

    for item in items:
        cards.append(
            {
                'title': item.find('div', class_='sklv-product-data').get_text(strip=True),
                'mech': item.find('div', class_='sklv-product-desc').find('p').get_text(strip=True).replace('\n', ''),
                'price': item.find('div', class_='sklv-prices').find('div', class_='sklv-prices__bottom').get_text(
                    strip=True),
                'rate': item.find('div', class_='sklv-product-rating').get_text(strip=True)
            }
        )
    return cards




def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Страна механизма', 'цена', 'колличество отзывов'])
        for item in items:
            writer.writerow([item['title'], item['mech'].rstrip('\n'), item['price'], item['rate']])


def parser():
    PAGE = input("skol'ko stranic? ")
    PAGE = int(PAGE.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for p in range(1, PAGE + 1):
            print(f'Парсим страницу: {p}')
            html = get_html(URL, params={'PAGE': p})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
    else:
        print('ERROR 404')

parser()
