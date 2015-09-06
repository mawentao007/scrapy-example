#coding:utf-8
__author__ = 'marvin'

import json
import re
from bs4 import BeautifulSoup

html = """<script>window.$config
window.$render_data = {  "stage":
                        {
                            "page":
                            {
                                "title":
                                {
                                    "txt": "全部微博",
                                    "txt_sub": false
                                }
                            }
                        }
                        };
</script>
"""

soup = BeautifulSoup(html,"lxml")
script = soup.find('script', text=re.compile('render_data'))
json_text = re.search(r'\$render_data\s*=\s*({.*?})\s*;$',
                      script.string, flags=re.DOTALL | re.MULTILINE).group(1)
print json_text
data = json.loads(json_text)
print data['stage']
# html = """<!doctype html>
# <title>extract javascript object as json</title>
# <script>
# // ..
# window.blog.data = {
#     "activity":
#             {
#                 "mod_type": {"type":"read"}
#             }
#
#         };
# </script>
# <p>some other html here
# """
# import json
# import re
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(html,"lxml")
# script = soup.find('script', text=re.compile('window\.blog\.data'))
# json_text = re.search(r'^\s*window\.blog\.data\s*=\s*({.*?})\s*;\s*$',
#                       script.string, flags=re.DOTALL | re.MULTILINE).group(1)
# data = json.loads(json_text)
# print data['activity']