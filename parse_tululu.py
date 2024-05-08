from pprint import pprint
from requests import HTTPError

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
                payload = {"id": f"{x+1}"}
                url = f"https://tululu.org/txt.php"
                response = requests.get(url, params=payload)
                print(response.history)
                check_for_redirect(response)
                filename = f'{x + 1}.txt'
                with open(filename, 'w') as file:
                     file.write(response.text)
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


