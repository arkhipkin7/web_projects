import requests

from typing import List, NoReturn
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand

from monitoring.models import Product, Search


def get_html(url: str) -> str:
    r = requests.get(url)
    return r.text


def get_total_pages(html: str) -> List:
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', class_='undefined c6e8ba5398--main-info--oWcMk')
    pages = []
    for result in divs:
        page = result.find('a', class_='c6e8ba5398--header--1fV2A').get('href')
        pages.append(page)
    return pages


def get_page_data(html: str, url: str, search) ->NoReturn:
    try:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1', class_='a10a3f92e9--title--2Widg')
        if title is None:
            title = 'Nope'
        else:
            title = title.text
        description = soup.find('p', class_='a10a3f92e9--description-text--3Sal4').text
        name_seller = soup.find('div', class_='a10a3f92e9--id--LA2Ew')
        if name_seller is None:
            name_seller = 'No name'
        else:
            name_seller = name_seller.text
        phone_number = soup.find('a', class_='a10a3f92e9--phone--3XYRR').text
        phone_number = phone_number.replace(' ', '').replace('-', '')
        image = soup.find('img', {'class': 'a10a3f92e9--photo--3ybE1'}).get('src')

        product = Product.objects.create(title=title, description=description, name_seller=name_seller,
                                         phone_number=phone_number, image=image, url=url, search=search)

        product.save()

        # print(f'title: {title}\n{descriptions[:10]}\n{name_seller}\n{phone_number}') # Debug ^^
    except ValueError:
        print('Запрос уже в базе')


class Command(BaseCommand):
    help = 'Парсинг ЦИАН'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='Ссылка на парсинг')
        parser.add_argument('pages', type=int, help='Кол-во страниц для парсинга')

    def handle(self, *args, **options):
        url = options['url']
        page_number = options['pages']

        search = Search()
        search.url = url
        search.pages = page_number
        search.save()

        for page in range(page_number):
            total_page_of_announ = get_total_pages(get_html(url + str(page)))
            for url in total_page_of_announ:
                print(f'Link page: {url}')
                get_page_data(get_html(url), url, search)
