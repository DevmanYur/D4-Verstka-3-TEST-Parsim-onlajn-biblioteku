import os
import argparse

import requests
from pathlib import Path
from requests import HTTPError
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_image(url, filename, folder='images/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    image_tag = soup.find(class_='bookimage').find('img')['src']
    image_way = urljoin('https://tululu.org/', image_tag)

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
    tittle_tag = soup.find('h1').text.split('::')
    tittle = f'{tittle_tag[0].strip()}'
    print(f'Заголовок: {tittle}')

    genre_tag = soup.find('span', class_='d_book').find_all('a')
    genres = []
    for genre in genre_tag:
        genres.append(genre.text)
    print(f'Жанр: {genres}')

    comments_tag = soup.find_all(class_='texts')
    comments = []
    for comment in comments_tag:
        comments.append(comment.find(class_='black').text)
    print(f'Комментарии: {comments}')


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def main():
    parser = argparse.ArgumentParser(
        description='Скачивание заданных страниц'
    )
    parser.add_argument('start_id', help='Страница с', type=int)
    parser.add_argument('end_id', help='Страница по', type=int)
    args = parser.parse_args()

    url = 'https://tululu.org/'

    for filename in range(args.start_id, args.end_id+1):
        try:

            payload = {'id': str(filename)}
            response = requests.get(f'{url}txt.php', params=payload)
            response.raise_for_status()

            check_for_redirect(response)

            response_book_page = requests.get(f'{url}b{filename}')
            response_book_page.raise_for_status()
            soup = BeautifulSoup(response_book_page.text, 'lxml')

            parse_book_page(soup)

            download_txt(response.url, filename)
            download_image(response_book_page.url, filename)


        except HTTPError:
            continue


if __name__ == '__main__':
    main()
