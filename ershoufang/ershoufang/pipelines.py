# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook

class ErshoufangPipeline(object):

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['区域','标题','小区','户型','面积','装修','电梯','楼层','楼龄','地铁','房本','地址','总价(万元)','单价(元/平米)','关注度', '发布时间','详情链接'])  # 设置表头


    def process_item(self, item, spider):

        for i in range(0,30):
            line = [item['district'][i], item['title'][i], item['block'][i], item['layout'][i], item['area'][i], item['direction'][i], item['elevator'][i], item['floor'][i], item['age'][i], item['subway'][i], item['taxfree'][i], item['location'][i], item['totalprice'][i], item['unitprice'][i], item['followers'][i], item['posttime'][i], item['detailpage'][i]]  # 把数据中每一项整理出来
            self.ws.append(line)

        self.wb.save('C:/Users/wangwi1/OneDrive - Mars Inc/Python/ershoufang/房价.xlsx')
        return item
