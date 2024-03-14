import os

import requests
from pathlib import Path
from requests import HTTPError
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import unquote


def download_comments(url):
    # Ссылка на страницу
    response = requests.get(url)
    response.raise_for_status()

    # Суп страницы
    soup = BeautifulSoup(response.text, 'lxml')

    # Ищем комментарий и вычисляем к ней путь
    comm_tag = soup.find_all(class_='texts')
    for x in comm_tag:
        print(x.find(class_='black').text)


def download_image(url, filename, folder='images/'):


    # Создаем папку
    Path(folder).mkdir(parents=True, exist_ok=True)

    # Ссылка на страницу
    response = requests.get(url)
    response.raise_for_status()

    # Суп страницы
    soup = BeautifulSoup(response.text, 'lxml')

    # Ищем картинку и вычисляем к ней путь
    image_tag = soup.find(class_='bookimage').find('img')['src']
    image_way = urljoin('https://tululu.org/', image_tag)
    print(image_way)

    # Ссылка на картинку
    response = requests.get(image_way)
    response.raise_for_status()

    way = os.path.join(folder, sanitize_filename(filename))
    filename_ = f'{way}.jpg'

    with open(filename_, 'wb') as file:
        file.write(response.content)


def download_txt(url, filename, folder='books/'):

    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    way = os.path.join(folder, sanitize_filename(filename))
    filename_ = f'{way}.txt'
    with open(filename_, 'w') as file:
        file.write(response.text)
    print(filename_)
    return filename_


def check_for_redirect(response, number):
    if response.history!=[]:
        print(f'{number}. Ответ пришёл с главной')
        raise HTTPError

def main():

    url = 'https://tululu.org/'

    for i in range(1, 11):
        try:
            payload = {'id': str(i)}
            response = requests.get(f'{url}txt.php', params=payload)
            response.raise_for_status()


            check_for_redirect(response, i)

            response2 = requests.get(f'{url}b{i}')
            response2.raise_for_status()

            soup = BeautifulSoup(response2.text, 'lxml')
            tittle_tag = soup.find('h1').text.split('::')
            tittle_name = f'{i}. {tittle_tag[0].strip()}'

            download_txt(response.url, tittle_name)


            download_image(response2.url, str(i))

            download_comments(response2.url)



            image_tag = soup.find(class_='bookimage').find('img')['src']
            image_way = urljoin('https://tululu.org/', image_tag)

            print(tittle_name)
            print('Сама страница', response2.url)
            print('Cтраница на текст скачивания',response.url)
            print('Путь до картинки',image_way)







        except HTTPError:
            continue


if __name__ == '__main__':
    main()