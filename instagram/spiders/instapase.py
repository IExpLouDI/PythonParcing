import scrapy
from scrapy.http import HtmlResponse
import re
import json
from instagram.items import InstagramItem
# from scrapy.loader import ItemLoader
# from copy import deepcopy


class InstapaseSpider(scrapy.Spider):
    name = 'instapase'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    log_user = "mrtomascats"
    us_pas = "#PWD_INSTAGRAM_BROWSER:10:1640380779:AaNQAI781VmjJWoavVTAqNqicf08/L7CLayDpzMWN3BwmJFC4PoPPUplWxqBrtWV1VTM1/tBX5rZONSKlpPhrovmsMSKBLM4f9aCTIUGQHGunCCH3qamBilvhBIoieU9CGUP6AOI4J0Zkauz4g=="
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    users = ['ninellska', 'vssuchkov']
    sections = ['followers', 'following']
    user_agent = "Instagram 155.0.0.37.107"


    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)

        yield scrapy.FormRequest(self.login_url,
                                 method="POST",
                                 callback=self.user_login,
                                 formdata={'username': self.log_user,
                                           'enc_password': self.us_pas},
                                 headers={'X-CSRFToken': csrf_token}
                                 )

    def user_login(self, response: HtmlResponse):

        j_data = response.json()
        if j_data.get("authenticated"):
            for user in self.users:
                url_follow = f"https://www.instagram.com/{user}/"
                yield response.follow(url_follow,
                                      callback=self.user_parse,
                                      cb_kwargs={"user": user}
                                      )

    def user_parse(self, response: HtmlResponse, user):
        user_id = self.fetch_user_id(response.text, user)
        for section in self.sections:
            yield scrapy.FormRequest(f'https://i.instagram.com/api/v1/friendships/{user_id}/{section}/?count=12',
                                     method="GET",
                                     headers={'User-Agent': self.user_agent},
                                     callback=self.get_follow,
                                     cb_kwargs={'name': user,
                                                'user_id': user_id,
                                                'section': section}
                                     )

    def get_follow(self, response: HtmlResponse, name, user_id, section):
        j_data = response.json()

        if j_data.get('next_max_id'):
            next_max_id = j_data.get('next_max_id')
            yield scrapy.FormRequest(f'https://i.instagram.com/api/v1/friendships/{user_id}/{section}/?count=12&max_id={next_max_id}',
                                     method="GET",
                                     headers={'User-Agent': self.user_agent},
                                     callback=self.get_follow,
                                     cb_kwargs={'name': name,
                                                'user_id': user_id,
                                                'section': section}
                                     )

        users = j_data.get('users')
        for user in users:
            item = InstagramItem(
                user_db=name,
                user_section=section,
                user_nick_name=user['username'],
                user_name=user['full_name'],
                user_id=user['pk'],
                user_img=user['profile_pic_url']
            )
            yield item

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')


