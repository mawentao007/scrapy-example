#encoding=utf-8
import scrapy
from tutorial.ScalaItem import ScalaItem

class ScalaSpider(scrapy.Spider):
        name = "scala"
        allowed_domains = ["scalaboy.top"]
        start_urls = [
             "http://www.scalaboy.top/index.html"
        ]

        def parse(self, response):
            #css方式选取元素
            for href in response.css(".item >.hentry > .index >a::attr('href')"):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_dir_contents)

        def parse_dir_contents(self, response):
            #xpath方式选取元素
            #encode('utf-8')修改编码方式
            for sel in response.xpath('//h4[@class="entry-title"]'):
                item = ScalaItem()
                item['title'] = sel.xpath('text()').extract()
                yield item






