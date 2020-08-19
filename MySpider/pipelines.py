# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from MySpider.items import ZycgModel


class MyspiderPipeline:
    def process_item(self, item, spider):
        ZycgModel.create(company=item['company'], name=item['name'],
                         address=item['address'], phone=item['phone'], mobile=item['mobile'])

        return item
