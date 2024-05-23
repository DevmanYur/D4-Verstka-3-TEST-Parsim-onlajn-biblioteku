import os
import argparse

import requests
from pathlib import Path
from requests import HTTPError
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse





def f1(url, page):
        try:
                url_txt = f"{url}/txt.php"
                payload_txt = {'id': page}
                response_txt = requests.get(url_txt, params=payload_txt)
                response_txt.raise_for_status()
                check_for_redirect(response_txt)

                # Страница
                response_page = requests.get(f'{url}/b{page}/')
                response_page.raise_for_status()
                check_for_redirect(response_page)

                # Суп страницы
                soup = BeautifulSoup(response_page.text, 'lxml')
                tittle, author, comments, genres, image, image_tag = parse_book_page(soup)
                print(parse_book_page(soup))


                url_image = f'{url}{image_tag}'
                response_image = requests.get(url_image)
                response_image.raise_for_status()







                download_txt(response_txt, f'{page}. {tittle}')
                download_images(response_image, image)
                download_comments(comments, f'{page}. {tittle} - комментарии')





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



def main():
    parser = argparse.ArgumentParser(
        description='Скачивание заданных страниц'
    )
    parser.add_argument('start_id', help='Страница с', type=int)
    parser.add_argument('end_id', help='Страница по', type=int)
    args = parser.parse_args()




    url = f"https://tululu.org"

    for page in range(args.start_id, args.end_id + 1):
        try:
            f1(url, page)
        except HTTPError:
            continue





if __name__ == '__main__':
    main()





