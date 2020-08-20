import scrapy
from MySpider.settings import USER_AGENT
from MySpider.items import ZycgItem
from copy import deepcopy


class ZycgSpider(scrapy.Spider):
    name = 'zycg'
    allowed_domains = ['oa.zycg.cn']
    base_url = 'http://oa.zycg.cn'
    start_urls = ['http://oa.zycg.cn/td_xxlcpxygh/platform']
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "oa.zycg.cn",
        "If-None-Match": "b36af75105a553724152a5f5db69b575",
        "Referer": "http://oa.zycg.cn/td_xxlcpxygh/platform",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": USER_AGENT
    }

    def parse(self, response, **kwargs):
        href_list = response.xpath('//td[@class="grade3"]/a')
        for href in href_list:
            url = self.base_url + href.xpath('./@href').get()
            yield scrapy.Request(url=url, callback=self.parse_brand, headers=self.headers)

    def parse_brand(self, response):
        brand_href = self.base_url + response.xpath('//div[@class="tzym"]/div/div['
                                                    '2]/table/tr/td/table/tr/td/table/tr/td/a['
                                                    '1]/@href').get()
        yield scrapy.Request(url=brand_href, callback=self.parse_all_brand)

    def parse_all_brand(self, response):
        href_list = response.xpath('//td[@class="Introduce_Info_Model"]/a/@href').getall()
        for href in href_list:
            url = self.base_url + href
            yield scrapy.Request(url=url, callback=self.parse_gys, headers=self.headers)
        next_page = response.xpath('//a[@class="next_page"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse_all_brand)

    def parse_gys(self, response):
        FDItemCode = eval(response.xpath('//div[@id="MainMeun"]/ul/li[2]/@onclick').get().split(',')[1])
        FDProductID = eval(response.xpath('//div[@id="MainMeun"]/ul/li[2]/@onclick').get().split(',')[2])

        for i in range(9, 40):
            url = 'http://oa.zycg.cn/td_xxlcpxygh/gys_info?FDProductID=' + FDProductID + \
                  '&FDItemCode=' + FDItemCode + '&SelectProvinse=' + str(i)
            yield scrapy.Request(url=url, callback=self.parse_province_gys, headers=self.headers)

    def parse_province_gys(self, response):
        gys_list = response.xpath('//table[@class="gys_bj"]/tbody/tr[position()>1]/td[5]/a/@href').getall()
        for href in gys_list:
            item = ZycgItem()
            item['company'] = response.xpath('//table[@class="gys_bj"]/tbody/tr[position()>1]/td[5]/a/text()').get().strip()
            url = self.base_url + '/gys_zs/gys_basic_info?GetWay=Ajax&id=' + href.split('/')[-1]
            yield scrapy.Request(url=url, callback=self.parse_item, headers=self.headers, meta={'item': deepcopy(item)})

    def parse_item(self, response):
        item = response.meta['item']
        item['name'] = response.xpath('//table[@class="gys_info"]/tr[7]/td[2]/text()').get()
        item['phone'] = response.xpath('//table[@class="gys_info"]/tr[8]/td[4]/text()').get()
        if item['phone'] is not None:
            item['phone'] = item['phone'].strip()
        item['mobile'] = response.xpath('//table[@class="gys_info"]/tr[9]/td[4]/text()').get()
        if item['mobile'] is not None:
            item['mobile'] = item['mobile'].strip()
        return item
