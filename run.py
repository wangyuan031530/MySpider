from scrapy.cmdline import execute
from MySpider.spiders.zycg import ZycgSpider

name = ZycgSpider.name
cmd = 'scrapy crawl {0}'.format(name)
execute(cmd.split())
