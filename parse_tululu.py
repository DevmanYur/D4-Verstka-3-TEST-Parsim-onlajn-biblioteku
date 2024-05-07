import os
import argparse

import requests
from pathlib import Path
from requests import HTTPError
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse


def check_for_tululu(url):
    if urlparse(url).netloc != 'tululu.org':
        print('Ответ пришел НЕ с сайта tululu.org')
        raise HTTPError


def download_image(filename, soup, folder='images/'):
    Path(folder).mkdir(parents=True, exist_ok=True)

    image_tag = soup.find(class_='bookimage').find('img')['src']
    image = urljoin('https://tululu.org/', image_tag)

    response_image = requests.get(image)
    response_image.raise_for_status()

    foldername = os.path.join(folder, sanitize_filename(str(filename)))
    filename_ = f'{foldername}.jpg'

    with open(filename_, 'wb') as file:
        file.write(response_image.content)


def download_txt(response, filename, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    foldername = os.path.join(folder, sanitize_filename(str(filename)))
    filename_path = f'{foldername}.txt'
    with open(filename_path, 'w') as file:
        file.write(response.text)
    return filename_path


def parse_book_page(soup):
    tittle_tag = soup.find('h1').text.split('::')
    tittle = f'{tittle_tag[0].strip()}'

    genre_tag = soup.find('span', class_='d_book').find_all('a')
    genres = []
    for genre in genre_tag:
        genres.append(genre.text)

    comments_tag = soup.find_all(class_='texts')
    comments = []
    for comment in comments_tag:
        comments.append(comment.find(class_='black').text)

    parse_book = [tittle, genres, comments]

    return parse_book


def check_for_redirect(response):
    if response.history:
        print('Ответ пришел с главной страницы')
        raise HTTPError


def main():
    parser = argparse.ArgumentParser(
        description='Скачивание заданных страниц'
    )
    parser.add_argument('start_id', help='Страница с', type=int)
    parser.add_argument('end_id', help='Страница по', type=int)
    args = parser.parse_args()

    url = 'https://tululu.org/'

    check_for_tululu(url)

    for page in range(args.start_id, args.end_id + 1):
        try:

            try:
                payload = {'id': str(page)}
                response = requests.get(f'{url}txt.php', params=payload)
                response.raise_for_status()

                check_for_redirect(response)

                book_page_response = requests.get(f'{url}b{page}')
                book_page_response.raise_for_status()
                soup = BeautifulSoup(book_page_response.text, 'lxml')

                print(parse_book_page(soup))

                download_txt(response, page)

                download_image(page, soup)

            except ConnectionError:
                continue


        except HTTPError:
            continue


if __name__ == '__main__':
    main()