# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from selenium import webdriver
from ..items import BookItem

class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['search.jd.com']
    page_url = 'https://search.jd.com/Search?keyword={keyword}&page={page}'
    keyword = 'python'
    page_total = 100

    def __init__(self):
        super().__init__(name=self.name)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        prefs = {'profile.default_content_setting_values': {'images': 2}}
        chrome_options.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.set_page_load_timeout(30)

    def closed(self, spider):
        print("spider closed")
        self.browser.close()

    def start_requests(self):
        for page in range(1, self.page_total*2+1, 2):
            url = self.page_url.format(keyword=self.keyword, page=page)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.css('.gl-warp .gl-item')
        print(len(items))
        if items:
            for item in items:
                book = BookItem()
                book['data_sku'] = item.xpath('./@data-sku').extract_first()
                book['name'] = item.css('.p-name').xpath('string(.//em)').extract_first()
                book['price'] = item.css('.p-price').xpath('string(.//strong)').extract_first()
                book['author'] = item.css('.p-bookdetails').xpath('string(.//span[@class="p-bi-name"])').extract_first()
                book['publishing_house'] = item.css('.p-bookdetails').xpath('string(.//span[@class="p-bi-store"])').extract_first()
                book['date'] = item.css('.p-bookdetails').xpath('string(.//span[@class="p-bi-date"])').extract_first()
                book['comments_count'] = item.css('.p-commit').xpath('string(.//strong)').extract_first()
                yield book

