# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

def is_article_loaded(div):
    try:
        div.find_element_by_css_selector('div.RichContent div.ContentItem-time a span')
        return True
    except NoSuchElementException:
        return False

class PhantomJSMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod

    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        self.driver = webdriver.PhantomJS()

    def spider_closed(self, spider):
        self.driver.close()

    def process_request(self, request, spider):
        request.meta['driver'] = self.driver
        self.driver.get(request.url)
        if request.url.split('/')[-1] == 'activities':
            WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'ProfileHeader-expandButton')]"))
            )
            self.driver.find_element_by_xpath('//button[contains(@class, "ProfileHeader-expandButton")]').click()
        if request.url.split('/')[-1].split('?')[0] == 'answers' or request.url.split('/')[-1].split('?')[0] == 'posts':
            WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'PlaceHolder')]"))
            )
            for div in self.driver.find_elements_by_css_selector('div.List-item div.ContentItem'):
                div.find_element_by_css_selector('div.RichContent div.RichContent-inner button').click()
                WebDriverWait(self.driver, 10).until(
                        lambda x: div.find_element_by_css_selector('div.RichContent div.ContentItem-time')
                )

        if request.url.split('/')[2] == 'zhuanlan.zhihu.com':
            pass

        body = to_bytes(self.driver.page_source)
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)
