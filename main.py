import os

import requests
from pathlib import Path
from requests import HTTPError
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup


def download_txt(url, filename, folder='books/'):

    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    way = os.path.join(folder, sanitize_filename(filename))
    filename_ = f'{way}.txt'
    with open(filename_, 'w') as file:
        file.write(response.text)
    return filename_


def check_for_redirect(response):
    if response.history!=[]:
        print("ответ пришёл с главной")
        raise HTTPError

def main():

    for i in range(1, 11):
        try:
            payload = {'id': str(i)}
            response = requests.get('https://tululu.org/txt.php', params=payload)
            response.raise_for_status()
            url = response.url

            check_for_redirect(response)

            url2 = f'https://tululu.org/b{i}'
            response2 = requests.get(url2)
            response2.raise_for_status()
            soup = BeautifulSoup(response2.text, 'lxml')
            title_tag = soup.find('h1')
            title_text = title_tag.text
            y = title_text.split('::')
            filename = f'{i}. {y[0].strip()}'
            print(filename)


            download_txt(url, filename)

        except HTTPError:
            continue


if __name__ == '__main__':
    main()