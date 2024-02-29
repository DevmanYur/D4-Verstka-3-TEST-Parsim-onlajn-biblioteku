import requests
from pathlib import Path

def get_book():

    name_folder = 'book'
    name_file = 'id'
    Path(name_folder).mkdir(parents=True, exist_ok=True)

    for i in range(1, 11):
        url = 'https://tululu.org/txt.php?id=' + str(i)
        response = requests.get(url)
        response.raise_for_status()
        filename = name_folder + '/' + name_file + str(i) + '.txt'
        with open(filename, 'w') as file:
            file.write(response.text)


if __name__ == '__main__':
    get_book()


