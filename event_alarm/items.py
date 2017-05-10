# -*- coding: utf-8 -*-

# 파싱할 데이터 구조 정의

import scrapy

class EventAlarmItem(scrapy.Item):
    id = scrapy.Field()      # 게시물 번호
    title = scrapy.Field()   # 게시물 제목
    date = scrapy.Field()    # 게시물 등록 날짜
