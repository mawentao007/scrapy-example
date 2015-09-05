# import requests
# import re
# from bs4 import BeautifulSoup
#
# user_agent = {'User-agent': 'spider'}
# r = requests.get("http://weibo.com/2175542711",headers=user_agent)
# p_nick = re.compile(r"CONFIG\['onick'\]='(.*?)'")
# m_nick = re.findall(p_nick,r.text)
# soup = BeautifulSoup(r.text)
# content = soup.find_all("div","WB_text W_f14")
# if len(m_nick) == 1:
#         for wb in content:
#             print wb.text
# else:
#         print "Not found!"