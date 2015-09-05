#encoding=utf-8





import scrapy
import re
import time
from tutorial.WeiboItem import WeiboItem

class WeiboSpider(scrapy.Spider):
        name = "googleWeibo"

        user_agent = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

        _cookie={"SUB":"_2A2547rshDeTxGeRP7FcU9CzLyj2IHXVYEMVprDV6PUJbrdAKLXH3kW2bdy6UqyJs-c8G8GcX7xITFuIkGg..",
                " SUHB":"0pHgiRk5AUsN1y",
                "_T_WM":"f3cd96c8a1bdcf92fe154ac20040a56e",
                "gsid_CTandWM":"4ulE23bf1M9obnQWHqZWv97Xobt"}


        def start_requests(self):
            return [scrapy.FormRequest("http://m.weibo.cn/page/json?containerid=1005051799756001_-_WEIBO_SECOND_PROFILE_WEIBO&page=1",
                                    headers=self.user_agent)]

        def parse(self, response):
            for  page in range(2,10):
                url = "http://m.weibo.cn/page/json?containerid=1005051799756001_-_WEIBO_SECOND_PROFILE_WEIBO&page=" + str(page)
                yield scrapy.Request(url,headers=self.user_agent,callback=self.parse_dir_contents)

        def parse_dir_contents(self, response):
            for sel in response.xpath('//span[@class="ctt"]'):
                item = WeiboItem()
                item['post'] = sel.xpath('text()').extract()[0].strip()
                yield item






