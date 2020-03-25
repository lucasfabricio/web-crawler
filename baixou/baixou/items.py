# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst, MapCompose
from lxml.html import unicode
from w3lib.html import remove_tags

def remove_query_string(link):
    
    url_splited = link.split('?')
    url = url_splited[0]
    
    return url

# Converte preço no formato 'R$ 1.000,00' para float => 1000.00
def parse_price(price):
    
    price = re.sub(r'[R$\. ]', '', price).replace(',', '.')

    return float(price)

class AmericanasItemLoader(ItemLoader):
    
    default_output_processor = TakeFirst()
    
    url_in = MapCompose(remove_query_string)
    category_in = MapCompose(unicode.title)
    description_in = MapCompose(remove_tags)
    price_in = MapCompose(parse_price)
    

class BaixouItem(scrapy.Item):
    
    url = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
