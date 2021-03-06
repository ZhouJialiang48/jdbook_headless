# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
import time

class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == 'jd_book':
            try:
                spider.browser.get(request.url)
                spider.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            except TimeoutException:
                print('超时')
                spider.browser.execute_script('window.stop()')
            time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                                encoding="utf-8", request=request)
