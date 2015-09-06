#encoding=utf-8





import scrapy
import re
import time
import json
from tutorial.WeiboItem import WeiboItem

class WeiboSpider(scrapy.Spider):
        name = "googleWeibo"

        user_agent = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}



        def start_requests(self):
            return [scrapy.FormRequest("http://m.weibo.cn/page/json?containerid=1005051799756001_-_WEIBO_SECOND_PROFILE_WEIBO&page=1",
                                    headers=self.user_agent)]

        def parse(self, response):
                jsonresponse = json.loads(response.body_as_unicode())
                for num in range(2,len(jsonresponse["cards"][0]["card_group"])):
                    mblog = jsonresponse["cards"][0]["card_group"][num]["mblog"]
                    item = WeiboItem()
                    if mblog.has_key("retweeted_status"):
                                    item["post"]=mblog["retweeted_status"]["text"]
                    else:
                                    item["post"]=mblog["text"]


                    yield item
            # for  page in range(1,2):
            #     url = "http://m.weibo.cn/page/json?containerid=1005051799756001_-_WEIBO_SECOND_PROFILE_WEIBO&page=" + str(page)
            #     yield scrapy.Request(url,headers=self.user_agent,callback=self.parse_dir_contents)

        def parse_dir_contents(self, response):
                jsonresponse = json.loads(response.body_as_unicode())
                for ans in jsonresponse["cards"]:
                    item = WeiboItem()
                    item["post"] = ans["mblog"]["text"]
                    yield item







