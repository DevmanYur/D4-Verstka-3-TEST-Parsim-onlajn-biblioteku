import os
from pprint import pprint
from requests import HTTPError
from pathlib import Path
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

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



                folder = 'books/'
                Path(folder).mkdir(parents=True, exist_ok=True)

                url_txt = "https://tululu.org/txt.php"
                payload_txt = {'id': x+1}
                response_txt = requests.get(url_txt, params=payload_txt)
                response_txt.raise_for_status()
                print(response_txt.url)
                check_for_redirect(response_txt)


                url_page = f"https://tululu.org/b{x+1}/"
                response_page = requests.get(url_page)
                response_page.raise_for_status()
                print(response_page.url)
                soup = BeautifulSoup(response_page.text, 'lxml')
                title_tag = soup.find('h1')
                tittle, author = soup.find('h1').text.split('::')

                sanitize_tittle = sanitize_filename(tittle.strip())
                print(sanitize_tittle)

                filename = f'{x+1}. {sanitize_tittle}'
                print(filename)



                foldername = os.path.join(folder, filename)
                filename_path = f'{foldername}.txt'
                with open(filename_path, 'w') as file:
                    file.write(response_txt.text)




            except HTTPError:
                print('continue')
                continue









def check_for_redirect(response):
            if response.history:
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


