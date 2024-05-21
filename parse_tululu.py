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
    folder = 'books/'
    Path(folder).mkdir(parents=True, exist_ok=True)
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


                # Заголовок
                tittle, author = soup.find('h1').text.split('::')
                sanitize_tittle = sanitize_filename(tittle.strip())


                # Картинка
                tag_image = soup.find(class_='bookimage').find('img')['src']
                url_image = f'{url}{tag_image}'
                response_image = requests.get(url_image)
                response_image.raise_for_status()

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







                name_file = f'{x+1}. {sanitize_tittle}'
                print(name_file)
                print('страница :', response_page.url)
                print('картинка :', url_image)
                print('тег картинка :', tag_image)
                name_image = tag_image.split('/')[-1]
                print(name_image)
                print('комментарии :', comments)
                print('жанр :', genres)
                print()

                folder_for_books = 'books'
                Path(folder_for_books).mkdir(parents=True, exist_ok=True)
                x = os.path.join(folder_for_books, name_file)
                y = f'{x}.txt'
                with open(y, 'w') as file:
                     file.write(response_txt.text)


                folder_for_images = 'images'
                Path(folder_for_images).mkdir(parents=True, exist_ok=True)
                z = os.path.join('images', name_image)
                q = f'{z}'
                with open(q, 'wb') as file2:
                    file2.write(response_image.content)

                folder_for_comments = 'comments'
                Path(folder_for_comments).mkdir(parents=True, exist_ok=True)
                r = os.path.join(folder_for_comments, f'{name_file} - комментарий')
                v = f'{r}.txt'
                with open(v, 'w') as file:
                    comments





        except HTTPError:
            print('continue')
            continue









def check_for_redirect(response):
            if response.history:
                print("Ссылка не действительна")
                raise HTTPError


f1 ()


    # text = response.text
    #
    #
    # filename = f'{x+1}.txt'
    # with open(filename, 'w') as file:
    #     file.write(text)
    #
    #
    #     def check_for_redirect(response):
    #         if response.history:
    #             print('Ответ пришел с главной страницы')
    #             raise HTTPError


# def download_txt(response, filename, folder='books/'):
#     Path(folder).mkdir(parents=True, exist_ok=True)
#     foldername = os.path.join(folder, sanitize_filename(str(filename)))
#     filename_path = f'{foldername}.txt'
#     with open(filename_path, 'w') as file:
#         file.write(response.text)


