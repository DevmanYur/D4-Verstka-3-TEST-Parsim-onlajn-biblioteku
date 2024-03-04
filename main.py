import requests
from pathlib import Path
from requests import HTTPError

def get_book():
    payload = {'id': '2'}
    url = 'https://tululu.org/txt.php'
    r = requests.get(url, params=payload)
    print(r.history)

    if r.history==[]:
        print("ответ пришёл с запрошенной страницы")
    else:
        print("ответ пришёл с главной")

if __name__ == '__main__':
    get_book()





    # try :
    #     if r.history==[]:
    #         print("good")
    #     else:
    #         print("bed")
    #
    # except OSError:
    #     print("bed2")
        # Инструкция raise без выражения поднимет FileNotFoundError повторно.
        # raise HTTPError

    # payload = {'id': '1'}
    # r = requests.get('https://tululu.org/txt.php', params=payload )
    # print(r.url)
    # print(r.history)


    # name_folder = 'book'
    # name_file = 'id'
    # Path(name_folder).mkdir(parents=True, exist_ok=True)
    #
    # for i in range(1, 11):
    #     url = 'https://tululu.org/txt.php?id=' + str(i)
    #     response = requests.get(url)
    #     response.raise_for_status()
    #     filename = name_folder + '/' + name_file + str(i) + '.txt'
    #     with open(filename, 'w') as file:
    #         file.write(response.text)




