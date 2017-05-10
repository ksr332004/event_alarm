# -*- coding: utf-8 -*-

__author__ = 'Seran'

from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from event_alarm.items import EventAlarmItem
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')


# scrapy crawl event


class EventSpider(InitSpider):
    name = "event"
    allowed_domains = ["www.temp-url.net"]
    login_page = "https://www.temp-url.net/Login"
    start_urls = "https://www.temp-url.net//Board/BoardList&id=01"

    login_id = 'your_id'
    login_pw = 'your_pw'

    def init_request(self):
        print("================ [init_request] =================")
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        obj = {
              'chkPC_SavedInfo': 'on'
            , 'hidUserAgentInfo': 'Chrome;1536*864;HTML5;OrderOS;'
            , '__VIEWSTATE': response.xpath('//input[contains(@name, "__VIEWSTATE")]/@value').extract_first()
        }
        obj['txtPC_LoginID'] = self.login_id
        obj['txtPC_LoginPW'] = self.login_pw

        return FormRequest.from_response(response,
                                          method="POST",
                                          formdata=obj,
                                          clickdata={'name': 'btnPC_Login'},
                                          callback=self.check_login_response)

    def check_login_response(self, response):
        print("================ [check_login_response] =================")
        if "logout" in response.body:
            print("================ [log in] =================")
            return self.initialized()
        elif "btnPC_Login" in response.body:
            print("================ [change password] =================")
            self.flag_pw = 1
            return self.login(response)
        else:
            print("================ [fail !!!] =================")
            return self.error()

    def initialized(self):
        return Request(url=self.start_urls, callback=self.parse_item, encoding='utf-8')

    def parse_item(self, response):
        print("================ [parse_item] =================")
        links = response.xpath('//table[contains(@id, "cphContent_cphContent_grid")]//tbody//tr')
        items = []
        for index, link in enumerate(links):
            item = EventAlarmItem()
            item['id'] = link.xpath('@messageid').extract_first()
            item['title'] = link.xpath('td[5]//p/@title').extract_first()
            item['date'] = link.xpath('td[11]/text()').extract_first()
            if (time.strftime("%Y.%m.%d") == item['date']) and ("영화" in item['title']):
                items.append(item)
        return items
