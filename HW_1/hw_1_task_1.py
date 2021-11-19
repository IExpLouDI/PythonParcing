import requests as rq
import json
from collections import defaultdict
from pprint import pprint


def repo_name(name):
    user = name
    url = f"https://api.github.com/users/{user}/repos"
    j_dict = defaultdict(list)

    response = rq.get(url)

    if response.ok is True:

        data = response.json()

        with open(f"{user}_repos.json", "w", encoding='utf-8') as f:

            for i in range(len(data)):
                j_dict['Repos_name'].append(data[i]['name'])

            json.dump(j_dict, f, ensure_ascii=False)

        return True

    return False


def opn_file(name):

    status = repo_name(name)

    if status is True:
        print(f'Файл с списком репозиториев пользователя {name} создан.\n'
              f'Проверяем содержимое файла: ')

        with open(f"{name}_repos.json", "r", encoding="utf-8") as f:
            decomp = json.load(f)
            pprint(decomp)

    else:
        print('Ошибка доступа')


us_name = input("Введите имя пользователя GitHub: ")

opn_file(us_name)