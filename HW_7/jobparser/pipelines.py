# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):

        if spider.name == 'hhru':
            final_salary = self.hhru_salary(item['salary'])
        else:
            final_salary = self.supjob_salary(item['salary'])

        item['min_salary'] = final_salary[0]
        item['max_salary'] = final_salary[1]
        item['currency'] = final_salary[2]
        del item['salary']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def supjob_salary(self, salary):

        temp = ' '.join(salary).replace('\xa0', '').split()

        if temp[0] == 'от':
            min_zp = int(temp[1][:-4])
            max_zp = None
            cur = temp[1][-4:]
        elif temp[0] == 'до':
            min_zp = None
            max_zp = int(temp[1][:-4])
            cur = temp[1][-4:]
        elif temp[0] == "По":
            min_zp = None
            max_zp = None
            cur = None
        elif len(temp) > 4:
            min_zp = int(temp[0])
            max_zp = int(temp[2])
            cur = temp[3]
        else:
            min_zp = temp[0]
            max_zp = None
            cur = temp[1]

        return min_zp, max_zp, cur

    def hhru_salary(self, salary):

        min_zp = None
        max_zp = None
        cur = None

        try:
            value = ' '.join(salary).replace('\xa0', '').split()

            if value[0] == 'от' and value[2] == 'до':
                min_zp = int(value[1])
                max_zp = int(value[3])
                cur = value[4]
            elif value[0] == 'от':
                min_zp = float(value[1])
                cur = value[2]
            elif value[0] == 'до':
                max_zp = float(value[1])
                cur = value[2]
            else:
                min_zp = float(value[0])
                max_zp = float(value[2])
                cur = value[3]
        finally:
            return min_zp, max_zp, cur
