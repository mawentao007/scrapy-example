#encoding=utf-8

import scrapy
import re
import time
import json
import re
from bs4 import BeautifulSoup
from tutorial.WeiboItem import WeiboItem



class WeiboSpider(scrapy.Spider):

#TODO 错误处理，失败的请求如何重新发起
        name = "googleWeibo"

#选取请求头部很重要，这里选取的是谷歌的爬虫头部
        user_agent = {'User-agent':'spider'}
        #user_agent = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

        #sumainUrl = "http://m.weibo.cn/u/2118407073"
        suurlBase = "http://m.weibo.cn/page/json?containerid=1005052118407073_-_WEIBO_SECOND_PROFILE_WEIBO&page="
        sufirstToParse = "http://m.weibo.cn/page/tpl?containerid=1005052118407073_-_WEIBO_SECOND_PROFILE_WEIBO&itemid=&title=%E5%85%A8%E9%83%A8%E5%BE%AE%E5%8D%9A"
        suMainUrl = "http://m.weibo.cn/u/2118407073"

        myurlBase = "http://m.weibo.cn/page/json?containerid=1005051799756001_-_WEIBO_SECOND_PROFILE_WEIBO&page="
        myfirstToParse = "http://m.weibo.cn/page/tpl?containerid=1005051799756001_-_WEIBO_SECOND_PROFILE_WEIBO&itemid=&title=%E5%85%A8%E9%83%A8%E5%BE%AE%E5%8D%9A"
        myMainUrl = "http://m.weibo.cn/u/1799756001"
#配置要抓取的url
        config = "u"
        if config is "su":
            urlBase = suurlBase
            firstToParse = sufirstToParse
            mainUrl = suMainUrl
        else:
            urlBase = myurlBase
            firstToParse = myfirstToParse
            mainUrl = myMainUrl

#第一个请求发出并获得结果，默认回调parse函数
        def start_requests(self):
            #起始url可以为空
            return [scrapy.FormRequest( self.mainUrl,
                                    headers=self.user_agent)]

        def parse(self, response):
            data = self.parse_html_json(response)
            postNumStr = data['stage']['page'][1]['mblogNum']     #获取微博总数并计算需要抓取的页面数量
            postNum = int(postNumStr)
            pageNum = (postNum % 10 + 9) / 10 + postNum/10

            #for  page in range(1,pageNum+1):
            for page in [305,320,343]:
                time.sleep(5)
                if page is 1:
                    yield scrapy.Request(self.firstToParse,headers=self.user_agent,callback=self.parse_html_contents)
                else:
                    url = self.urlBase + str(page)
                    yield scrapy.Request(url,headers=self.user_agent,callback=self.parse_json_contents)


#该函数首先通过soup从html中解析出包含json数据的元素
#之后通过re将相应的json字符串获取到
#最后利用json将其载入

        def parse_html_json(self,response):
                soup = BeautifulSoup(response.body_as_unicode(),"lxml")
                script = soup.find('script', text=re.compile('render_data'))
                #注意json必须要双引号
                json_text = re.search(r'\$render_data\s*=\s*({.*?})\s*;$',
                       script.string, flags=re.DOTALL | re.MULTILINE).group(1).replace("'", '"')
                data = json.loads(json_text)
                return data


#解析包含json的html的页面的内容，要调用parse_html_json
        def parse_html_contents(self,response):
                data = self.parse_html_json(response)
                for num in range(0,len(data['stage']['page'][1]['card_group'])):
                     item = WeiboItem()
                     mblog = data['stage']['page'][1]['card_group'][num]['mblog']
                     if mblog.has_key("retweeted_status"):
                        item['post'] = mblog['text']
                        item['repost'] = mblog['retweeted_status']['text']
                     else:
                        item['post'] = mblog['text']
                        item['repost'] = None
                     yield item


#解析response为json类型数据
        def parse_json_contents(self, response):
                jsonresponse = json.loads(response.body_as_unicode())
                for num in range(0,len(jsonresponse["cards"][0]["card_group"])):
                    mblog = jsonresponse["cards"][0]["card_group"][num]["mblog"]
                    item = WeiboItem()
                    if mblog.has_key("retweeted_status"):
                                    item["repost"]=mblog["retweeted_status"]["text"]
                                    item["post"] = mblog["text"]
                    else:
                                    item["post"]=mblog["text"]
                                    item["repost"] = None
                    yield item








