import requests as rq
import json
from collections import defaultdict
from pprint import pprint



ac_token = 'TOKEN'
user_id = 'YOUR_ID'
url = f"https://api.vk.com/method/groups.get?user_ids={user_id}&extended=1&v=5.131&access_token={ac_token}"
j_dict = defaultdict(list)
response = rq.get(url)

if response.ok is True:
    j_date = response.json()['response']['items']


    for i in range(len(j_date)):
        j_dict['Group_name'].append(j_date[i]['name'])

    with open("vk_group.json", "w", encoding="utf-8") as f:
        json.dump(j_dict, f, ensure_ascii=False)

    with open("vk_group.json", "r", encoding="utf-8") as f:
        temp = json.load(f)
        pprint(temp)
else:
    print('Error')
