# -*- coding: utf-8 -*-
import scrapy
from ershoufang.items import ErshoufangItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
import re

class ErshoufangSpider(scrapy.Spider):

    name = 'ershoufang'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://gz.lianjia.com/ershoufang/yuexiu/pg1/',
                  'https://gz.lianjia.com/ershoufang/tianhe/pg1/',
                  'https://gz.lianjia.com/ershoufang/huangpugz/pg1/',
                  'https://gz.lianjia.com/ershoufang/baiyun/pg1/',
                  'https://gz.lianjia.com/ershoufang/panyu/pg1/',
                  'https://gz.lianjia.com/ershoufang/nansha/pg1/',
                  'https://gz.lianjia.com/ershoufang/haizhu/pg1/',
                  'https://gz.lianjia.com/ershoufang/huadu/pg1/',
                  'https://gz.lianjia.com/ershoufang/liwan/pg1/'
                  ]

    def parse(self, response):

        """This function parses a property page.

        @url https://gz.lianjia.com/ershoufang/tianhe/
        @returns items 1
        @scrapes title block layout area direction location floor age totalprice unitprice posttime visitors
        @scrapes url project spider server date

        """
        l = ItemLoader(item = ErshoufangItem(), response = response)

        l.add_xpath('title', ".//div[@class='title']/a[@class='']/text()")
        l.add_xpath('block', ".//div[@class='houseInfo']/a/text()")

        layout = []
        area = []
        direction = []
        decoration = []
        elevator = []
        houseinfo = response.xpath(".//div[@class='houseInfo']/text()")
        for i in range(0,30):
            houseinfosplit = str(houseinfo[i].extract()).split(sep = '|')
            layout.append(houseinfosplit[1])
            area.append(houseinfosplit[2])
            direction.append(houseinfosplit[3])
            decoration.append(houseinfosplit[4])
            try:
                elevator.append(houseinfosplit[5])
            except:
                elevator.append(' ')

        l.add_value('layout', layout)
        l.add_value('area', area)
        l.add_value('direction', direction)
        l.add_value('decoration', decoration)
        l.add_value('elevator', elevator)
        l.add_xpath('totalprice', ".//div[@class='totalPrice']/span/text()")
        l.add_xpath('detailpage', ".//div[@class='title']/a/@href")
        l.add_xpath('location', ".//div[@class='positionInfo']/a/text()")

        floor = []
        age = []
        positioninfo = response.xpath(".//div[@class='positionInfo']/text()").extract()
        for j in range(0,30):
            try:
                floor.append(re.search(r'([\u4f4e\u4e2d\u9ad8]\u697c\u5c42\(\u5171[\d]+?\u5c42\))', str(positioninfo[j])).group())
            except:
                floor.append(' ')
            try:
                age.append(re.search(r'(\d{4}\u5e74\u5efa\u5854\u697c)', str(positioninfo[j])).group())
            except:
                age.append(' ')

        l.add_value('floor', floor)
        l.add_value('age', age)

        followinfo = response.xpath(".//div[@class='followInfo']/text()").extract()
        followers = []
        posttime = []
        for k in range(0,30):
            followinfosplit = str(followinfo[k]).split(sep = '/')
            posttime.append(followinfosplit[2])
            followers.append(re.search(r'(.+?\u770b)', str(followinfo[k])).group(1))

        l.add_value('posttime', posttime)
        l.add_value('followers', followers)

        taxfree = []
        xpath0 = ".//li[@class='clear'][{}]//span[@class='taxfree']/text()"
        for n in range(1,31):
            xpath = xpath0.format(n)
            a = response.xpath(xpath).extract()
            if a == []:
                taxfree.append(' ')
            else:
                taxfree.append(a[0])

        l.add_value('taxfree', taxfree)

        subway = []
        xpath1 = ".//li[@class='clear'][{}]//span[@class='subway']/text()"
        for m in range(1, 31):
            xpath = xpath1.format(m)
            b = response.xpath(xpath).extract()
            if b == []:
                subway.append(' ')
            else:
                subway.append(b[0])

        l.add_value('subway', subway)


        unitprice = []
        price = response.xpath(".//div[@class='unitPrice']/span/text()")
        for p in range(0,30):
            unitprice.append(re.search(r'(\d+)',str(price[p])).group())

        l.add_value('unitprice', unitprice)

        #根据网页地址信息识别区域
        district = []
        url = str(response.url)
        for o in range(0,30):
            urlsplit = url.split(sep = '/')
            if urlsplit[4] == 'tianhe':
                district.append(u'天河')
            elif urlsplit[4] == 'yuexiu':
                district.append(u'越秀')
            elif urlsplit[4] == 'liwan':
                district.append(u'荔湾')
            elif urlsplit[4] == 'haizhu':
                district.append(u'海珠')
            elif urlsplit[4] == 'baiyun':
                district.append(u'白云')
            elif urlsplit[4] == 'huangpugz':
                district.append(u'黄埔')
            elif urlsplit[4] == 'huadu':
                district.append(u'花都')
            elif urlsplit[4] == 'nansha':
                district.append(u'南沙')
            elif urlsplit[4] == 'panyu':
                district.append(u'番禺')

        l.add_value('district', district)

        yield l.load_item()

        #自动翻页
        page = response.xpath("//div[@class='page-box house-lst-page-box'][@page-data]").re("\d+")
        p = re.compile(r'[^\d]+')
        if len(page) > 1 and page[0] != page[1]:
            next_page = p.match(response.url).group() + str(int(page[1]) + 1) + '/'
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


