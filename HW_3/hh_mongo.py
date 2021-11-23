from pymongo import MongoClient
import requests as rq
from bs4 import BeautifulSoup
from pprint import pprint


def zp_check(value):
    z_min = None
    z_max = None
    ue = None

    try:
        value = value.getText().replace('\u202f', '').split()
        if value[0] == 'от':
            z_min = float(value[1])
            ue = value[2]
        elif value[0] == 'до':
            z_max = float(value[1])
            ue = value[2]
        else:
            z_min = float(value[0])
            z_max = float(value[2])
            ue = value[3]

    finally:

        return z_min, z_max, ue


def mongo_index(vacan):

    last_index = index[-1]
    index.append(last_index + 1)

    return last_index


def mongo_start_db():
    client = MongoClient('127.0.0.1', 27017)
    db = client['headhunter']

    return db.headhunter


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/96.0.4664.45 Safari/537.36'}
url = "https://hh.ru"
params = {'text': None,
          'area': 113, 'search_field': 'description', 'page': 0}

item = 0
i = 0
params['text'] = input('Введите название проффессии: ')
response = rq.get(url + '/search/vacancy/', params=params, headers=headers)
dom = BeautifulSoup(response.text, 'html.parser')
db_vacancy = mongo_start_db()
db_vacancy.delete_many({})

try:
    page = int(dom.find_all('span', {'class': 'pager-item-not-in-short-range'})[-1].getText())
except:
    page = 1

while i < page:
    if item == 5:
        break
    vacansies = dom.find_all('div', {'class': 'vacancy-serp-item'})

    for vacansy in vacansies:
        vac_dict = dict()

        name = vacansy.find('a').getText()
        link = vacansy.find('a')['href']
        zp = vacansy.find('div', {'class': 'vacancy-serp-item__sidebar'})

        vac_dict['_id'] = mongo_index(index)
        vac_dict['1_Name'] = name
        vac_dict['2_Min_ZP.'], vac_dict['3_Max_ZP.'], vac_dict['4_UE'] = zp_check(zp)
        vac_dict['5_Link'] = link[:link.index('?')]

        item += 1
        db_vacancy.insert_one(vac_dict)

        if item == 5:
            break

    i += 1
    params['page'] = i
    response = rq.get(url + '/search/vacancy/', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')

for item in db_vacancy.find({}):
    pprint(item)
# count = int(input(f'Сколько записей вывести на экран от 1 до {len(vac_list)}? '))
# for i in range(count):
#     print('*' * 40, '\n', f'№-{i + 1}')
#     pprint(vac_list[i])
#     print('*' * 40)