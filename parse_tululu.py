import os
import urllib
from pprint import pprint
from requests import HTTPError
from pathlib import Path
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from os.path import splitext
from urllib.parse import urlparse

import requests


# url = "https://tululu.org/txt.php?id=32168"
#
# response = requests.get(url)
# response.raise_for_status()
# text = response.text
#
#
# filename = 'text.txt'
# with open(filename, 'w') as file:
#     file.write(text)
#
#


def f1 ():
    url = f"https://tululu.org"

    for x in range(10):
        try:
                #шаг 8



                # Текст
                url_txt = f"{url}/txt.php"
                payload_txt = {'id': x+1}
                response_txt = requests.get(url_txt, params=payload_txt)
                response_txt.raise_for_status()
                check_for_redirect(response_txt)

                # Страница
                response_page = requests.get(f'{url}/b{x+1}/')
                response_page.raise_for_status()
                check_for_redirect(response_page)

                # Суп страницы
                soup = BeautifulSoup(response_page.text, 'lxml')
                tittle, author, comments, genres, image, image_tag = parse_book_page(soup)
                print(parse_book_page(soup))


                url_image = f'{url}{image_tag}'
                response_image = requests.get(url_image)
                response_image.raise_for_status()







                download_txt(response_txt, f'{x+1}. {tittle}')
                download_images(response_image, image)
                download_comments(comments, f'{x+1}. {tittle} - комментарии')





        except HTTPError:

            continue









def check_for_redirect(response):
            if response.history:

                raise HTTPError




def download_txt(url, filename, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filepath_without_format = os.path.join(folder, sanitize_filename(filename))
    filepath = f'{filepath_without_format}.txt'
    with open(filepath, 'w') as file:
        file.write(url.text)
    return filepath

def download_images(url, filename, folder='images/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(folder, sanitize_filename(filename))
    with open(filepath, 'wb') as file:
        file.write(url.content)
    return filepath

def download_comments(comments, filename, folder='comments/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filepath_without_format = os.path.join(folder, sanitize_filename(filename))
    filepath = f'{filepath_without_format}.txt'
    with open(filepath, 'w') : comments
    return filepath

def parse_book_page(soup):
    # Заголовок
    tittle2, author2 = soup.find('h1').text.split('::')
    tittle = sanitize_filename(tittle2.strip())
    author = sanitize_filename(author2.strip())

    # Комментарии
    comments_tag = soup.find_all(class_='texts')
    comments = []
    for comment in comments_tag:
        comments.append(comment.find(class_='black').text)

    # Жанр
    genre_tag = soup.find('span', class_='d_book').find_all('a')
    genres = []
    for genre in genre_tag:
        genres.append(genre.text)

    # Картинка
    image_tag = soup.find(class_='bookimage').find('img')['src']
    image = image_tag.split('/')[-1]


    return tittle, author, comments, genres, image, image_tag



f1 ()

