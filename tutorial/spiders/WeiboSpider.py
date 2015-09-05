#encoding=utf-8

#一个初级版本，使用自己的cookie，爬.cn下的数据。cookie请自行获取谢谢。


import scrapy
import time
from tutorial.WeiboItem import WeiboItem

class WeiboSpider(scrapy.Spider):
        name = "weibo"

        #必须感谢想出这个办法的人，模仿搜索引擎，爬取pc版有效，但是pc版要解析js
        #user_agent = {'User-agent': 'spider'}


        _cookie={"SUB":"_2A2547rshDeTxGeRP7FcU9CzLyj2IHXVYEMVprDV6PUJbrdAKLXH3kW2bdy6UqyJs-c8G8GcX7xITFuIkGg..",
                " SUHB":"0pHgiRk5AUsN1y",
                "_T_WM":"f3cd96c8a1bdcf92fe154ac20040a56e",
                "gsid_CTandWM":"4ulE23bf1M9obnQWHqZWv97Xobt"}


        def start_requests(self):
            return [scrapy.FormRequest("http://weibo.cn/1799756001",
                                   cookies=self._cookie)]

        def parse(self, response):
            #css方式选取元素
            #注意爬取手机版，.cn后缀
            for  page in range(1,10):
                time.sleep(1)
                url = "http://weibo.cn/1799756001/profile?page=" + str(page)
                yield scrapy.Request(url,cookies=self._cookie,callback=self.parse_dir_contents)

        def parse_dir_contents(self, response):
            #xpath方式选取元素
            #encode('utf-8')修改编码方式
            for sel in response.xpath('//span[@class="ctt"]'):
                item = WeiboItem()
                #strip(),清除空白；匹配字符串用的不太好
                item['post'] = sel.xpath('text()').extract()[0].strip()
                yield item


        #获取相关熟悉参数用@
        # for href in response.xpath('//a[@bpfilter="page"]/@href'):
            #     url = response.urljoin(href.extract())
            #     # yield scrapy.Request(url, callback=self.parse_dir_contents)
            #     print url




