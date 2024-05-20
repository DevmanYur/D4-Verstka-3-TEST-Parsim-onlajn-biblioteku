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

        for x in range(10):
            try:
                #шаг 8

                url = f"https://tululu.org"



                folder = 'books/'
                Path(folder).mkdir(parents=True, exist_ok=True)

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






                name_file = f'{x+1}. {sanitize_tittle}'
                print(name_file)
                print('страница :', response_page.url)
                print('картинка :', url_image)
                print('тег картинка :', tag_image)
                name_image = tag_image.split('/')[-1]
                print(name_image)
                print()


                x = os.path.join(folder, name_file)
                y = f'{x}.txt'
                with open(y, 'w') as file:
                     file.write(response_txt.text)

                z = os.path.join(folder, name_image)
                q = f'{z}'
                with open(q, 'wb') as file2:
                    file2.write(response_image.content)





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


