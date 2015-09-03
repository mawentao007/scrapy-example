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
            for href in response.css(".item >.hentry > .index >a::attr('href')"):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_dir_contents)

        def parse_dir_contents(self, response):
            for sel in response.xpath('//h4[@class="entry-title"]'):
                item = ScalaItem()
                item['title'] = sel.xpath('text()').extract()
                yield item


        # def parse(self, response):
        #     f = open('test', 'w')
        #     for sel in response.xpath('//ul/li'):
        #         title = sel.xpath('a/text()').extract()
        #         link = sel.xpath('a/@href').extract()
        #         desc = sel.xpath('text()').extract()
        #         print title, link, desc
        #         f.write('[' + ''.join(title).encode('utf8')+']\n')
        #     f.close()





        # def parse(self, response):
        #     for sel in response.xpath('//ul/li'):
        #         item = TutorialItem()
        #         item['title'] = sel.xpath('a/text()').extract()
        #         item['link'] = sel.xpath('a/@href').extract()
        #         item['desc'] = sel.xpath('text()').extract()
        #         yield item