# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from baixou.items import BaixouItem, AmericanasItemLoader

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AmericanasSpider(CrawlSpider):
    name = 'americanas'
    allowed_domains = ['americanas.com.br']
    start_urls = ['https://www.americanas.com.br/mapa-do-site']
    #base_url = 'https://www.americanas.com.br'

    rules = (
        Rule(
            LinkExtractor(allow='/categoria')
        ),
        Rule(
            LinkExtractor(allow='/produto'),
            callback='parse_details'
        )
    )

    def parse_details(self, response):

        loader = AmericanasItemLoader(item=BaixouItem(), response=response)
        
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//h1[@id="product-name-default"]/text()')
        loader.add_xpath('category', '//*[@id="content"]/div/div/div[2]/div/section/div/div[1]/div/div[2]/a/div/span/text()')
        loader.add_xpath('price', '//*[contains(@class, "price__SalesPrice")]/text()')
        loader.add_xpath('description', '//*[contains(@class, "info-description-frame-inside")]')

        yield loader.load_item()

class AmericanasManualSpider(scrapy.Spider):
    name = 'americanasManual'
    allowed_domains = ['americanas.com.br']
    start_urls = ['https://www.americanas.com.br/mapa-do-site']
    base_url = 'https://www.americanas.com.br'

    # Listagem de categorias
    def parse(self, response):
        items = response.xpath('//*[@class="sitemap-item"]')
        
        for item in items:
            href = item.xpath('.//a/@href').extract_first()
            url = self.urlBuilder(href)
            
            yield scrapy.Request(url, self.parse_category_list)

    # Listagem da categoria
    def parse_category_list(self, response):
        
        loader = AmericanasItemLoader(BaixouItem(), response=response)
        
        loader.add_value('url', response.url)
        loader.add_xpath('title', './/h2/text()')
        loader.add_xpath('category', '//ol[contains(@class,"breadcrumb")]/li[2]/a/span/text()')

        items = response.xpath('//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div')
        category = response.xpath('//ol[contains(@class,"breadcrumb")]/li[2]/a/span/text()').extract_first()

        for item in items:
            href = href = item.xpath('.//a/@href').extract_first()
            url = self.urlBuilder(href)
            title = item.xpath('.//h2/text()').extract_first()
            #price = item.xpath('.//span[starts-with(@class, "PriceUI-")]/text()').re(r'[\d]+,[\d]{2}')

            yield {
                'url': url,
                'title': title,
                'category': category
            }

        # Paginação
        next_page = response.xpath('//span[@aria-label="Next"]/../@href')

        if next_page:
            href = next_page.extract_first()
            url = self.urlBuilder(href)

            yield scrapy.Request(url, self.parse_category_list)

    def urlBuilder(self, relativePath):
        return "%s%s" % (self.base_url, relativePath)

