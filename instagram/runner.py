from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient
from pprint import pprint

from instagram import settings
from instagram.spiders.instapase import InstapaseSpider


def check_user_followers(user_ch, database):
    """Возвращает список подписчиков"""
    __users = ['vssuchkov', 'ninellska']
    condition = {'$and': [{'user_db': __users[int(user_ch) - 1]}, {'user_section': 'followers'}]}
    user_list = database.find(condition)
    print('Список подписчиков')
    return user_list


def check_user_following(user_ch, database):
    """Возвращает список подписоко"""
    __users = ['vssuchkov', 'ninellska']
    condition = {'$and': [{'user_db': __users[int(user_ch) - 1]}, {'user_section': 'following'}]}
    user_list = database.find(condition)
    print('Список подписок')
    return user_list


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.instagram.instapase

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstapaseSpider)

    process.start()

    user = input("Выберите пользователя:\n1 - VSSuchkov:\n2 - Ninellska.\n")

    for el in check_user_followers(user, db):
        pprint(el)

    print('*' * 40)

    for el in check_user_following(user, db):
        pprint(el)
