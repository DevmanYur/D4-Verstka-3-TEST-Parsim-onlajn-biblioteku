import os

import requests
from pathlib import Path
from requests import HTTPError
from pathvalidate import sanitize_filename


def download_txt(url, filename, folder='books/'):

    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    way = os.path.join(folder, sanitize_filename(filename))
    filename_ = f'{way}.txt'
    with open(filename_, 'w') as file:
        file.write(response.text)
    return filename_




url = 'http://tululu.org/txt.php?id=1'

filepath = download_txt(url, 'Алиби')
print(filepath)  # Выведется books/Алиби.txt

filepath = download_txt(url, 'Али/би', folder='books/')
print(filepath)  # Выведется books/Алиби.txt

filepath = download_txt(url, 'Али\\би', folder='txt/')
print(filepath)  # Выведется txt/Алиби.txt

# def check_for_redirect(response):
#     if response.history!=[]:
#         print("ответ пришёл с главной")
#         raise HTTPError
#
# def main():
#     name_folder = 'book'
#     name_file = 'id'
#     Path(name_folder).mkdir(parents=True, exist_ok=True)
#     for i in range(1, 11):
#         try:
#             payload = {'id': str(i)}
#             response = requests.get('https://tululu.org/txt.php', params=payload)
#             response.raise_for_status()
#             check_for_redirect(response)
#             filename = f'{name_folder}/{name_file}{str(i)}.txt'
#             with open(filename, 'w') as file:
#                 file.write(response.text)
#             print('try', i)
#
#         except HTTPError:
#             print('except', i)
#             continue

#
# if __name__ == '__main__':
#     main()

# def get():
#     import requests
#
#     url = 'https://tululu.org/b1/'
#     response = requests.get(url)
#     response.raise_for_status()
#
#     soup = BeautifulSoup(response.text, 'lxml')
#     title_tag = soup.find('h1')
#     title_text = title_tag.text
#
#     y = title_text.split('::')
#     print("Заголовок:",y[0].strip())
#     print("Автор:", y[0].strip())
