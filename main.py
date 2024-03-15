import os

import requests
from pathlib import Path
from requests import HTTPError
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import unquote


def download_image(url, filename, folder='images/'):

    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    image_tag = soup.find(class_='bookimage').find('img')['src']
    image_way = urljoin('https://tululu.org/', image_tag)
    print(image_way)

    response_image_way = requests.get(image_way)
    response_image_way.raise_for_status()

    way = os.path.join(folder, sanitize_filename(str(filename)))
    filename_ = f'{way}.jpg'

    with open(filename_, 'wb') as file:
        file.write(response_image_way.content)


def download_txt(url, filename, folder='books/'):

    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    way = os.path.join(folder, sanitize_filename(str(filename)))
    way_filename = f'{way}.txt'
    with open(way_filename, 'w') as file:
        file.write(response.text)
    return way_filename



def parse_book_page(soup):

    # Заголовок
    tittle_tag = soup.find('h1').text.split('::')
    tittle = f'{tittle_tag[0].strip()}'
    print(f'Заголовок: {tittle}')

    # Жанр
    genre_tag = soup.find('span', class_='d_book').find_all('a')
    genres =[]
    for genre in genre_tag :
        genres.append(genre.text)
    print(f'Жанр: {genres}')

    # Комментарии
    comments_tag = soup.find_all(class_='texts')
    comments = []
    for comment in comments_tag:
        comments.append(comment.find(class_='black').text)
    print(f'Комментарии: {comments}')





def check_for_redirect(response):
    if response.history!=[]:
        raise HTTPError

def main():

    url = 'https://tululu.org/'
    list = [5]

    for filename in list:
        try:

            # Страница загрузки txt файла
            payload = {'id': str(filename)}
            response = requests.get(f'{url}txt.php', params=payload)
            response.raise_for_status()
            print(response.url)

            # Проверка на редирект
            check_for_redirect(response)

            # Страница книги xml
            response_book_page = requests.get(f'{url}b{filename}')
            response_book_page.raise_for_status()
            print(response_book_page.url)
            soup = BeautifulSoup(response_book_page.text, 'lxml')

            # Запуск функции на парсинг
            parse_book_page(soup)

            # Запуск функции на скачивание текста
            download_txt(response.url, filename)
            download_image(response_book_page.url, filename)


        except HTTPError:
            continue


if __name__ == '__main__':
    main()