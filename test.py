import requests
import re

url = 'http://oa.zycg.cn/td_xxlcpxygh/products_by_brand?itemcode=GC-HG1180392-Y&category_id=7490&brand=all&page=1'

response = requests.get(url=url).text

