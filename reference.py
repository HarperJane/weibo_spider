
import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')
if(len(sys.argv)&gt;=2):
	user_id = (int)(sys.argv[1])
else:
	user_id = (int)(raw_input(u"please input user_id"))

cookie = {"Cookie":"_s_tentry=-; Apache=9576304049493.322.1459611446325; SINAGLOBAL=9576304049493.322.1459611446325; ULV=1459611446487:1:1:1:9576304049493.322.1459611446325:; SUS=SID-1342002822-1459611506-GZ-bl80g-d1fb7ec4b3c2ebb428b8f278ce5ceba3; SUE=es%3D0e0982a959b779984d535e729adda816%26ev%3Dv1%26es2%3Debef87c3ee2e64276c35265129db6a2f%26rs0%3DAHKl60KEySJqVoxoYmMCAtjKzRpMByO7CfL2WLjxIKVMZRRuXKWwy8xHA6JoRRQUXGr59JenwZOSTUBjnTKFySbWWjTZy6rGjpwtNaQag1JCdVrJfkNhNverqJjWaxDgPPYPinaS8rbrb9fKf82ubHYNwsF3pkdbI6gU7Xi4DLQ%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1459611506%26et%3D1459697906%26d%3Dc909%26i%3Deba3%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D2%26st%3D0%26uid%3D1342002822%26name%3Dpennying1990%2540sina.com%26nick%3DMillo%26fmp%3D%26lcp%3D; SUB=_2A257-5ciDeRxGedN71AR8CzEyT6IHXVZcI_qrDV8PUNbuNBeLXj9kW9LHeufzCSger4uE22dfgcltxARt2cJHg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFaqgNvq-ZBem2B9sp0na5.5JpX5K2t; SUHB=0xnDouttZmOfpz; ALF=1460216307; SSOLoginState=1459611506; un=pennybenny; wvr=6"}


url = 'http://weibo.com/u/%d?filter=1&amp;page=1'%user_id

html = requests.get(url, cookies = cookie).content

selector = etree.HTML(html)
pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

result = ''
urllist_set = set()
word_count = 1
image_count = 1

print u'爬虫准备就绪。。。'

#获取XML页面
url = 'http://weibo.com/u/%d?filter=1&amp;page=%d'%(user_id,page)
lxml = requests.get(url, cookies=cookie).content

#文字爬取
selector = etree.HTML(lxml)
content = selector.xpath('//span[@class="ctt"]')
for each in content:
	text = each.xpath('string(.)')
else:
	text = text+"\n\n"
result = result + text
word_count += 1

#图片爬取
soup = BeautifulSoup(lxml, "lxml")
urllist = soup.find_all('a', href=re.compile(r'^http://weibo.com/mblog/oripic',re.l))
first = 0
for imgurl in urllist:
	urllist_set.add(requests.get(imgurl['href'], cookies = cookie).url)
	image_count += 1

fo = open("/Users/Personals/%s"%user_id, "wb")
fo.write(result)
word_path = os.getcwd()+'/%d'%user_id
print u'文字微博爬取完毕'

link = ""
fo2 = open("/Users/Personals/%s_imageurls"%user_id, "wb")
for eachlink in urllist_set:
	link = link + eachlink + "\n"
fo2.write(link)
print u'图片链接爬取完毕'

if not urllist_set:
	print u'该页面不存在图片'
else:
	#下载图片，保存在当前目录的pythonimg文件夹下
	image_path = os.getcwd() + '/weibo_image'
	if os.path.exists(image_path) is False:
		os.mkdir(image_path)
	x = 1
	for imgurl in urllist_set:
		temp = image_path + '/%s.jpg'%x
		print u'正在下载%s张图片'%x
		try:
			urllib.urlretrieve(urllib2.urlopen(imgurl).geturl().temp)
		except:
			print u"该图片下载失败"%imgurl
		x += 1

print u"原创微博爬取完毕，共%d条，保存路径%s'%(word_count-4,word_path)
print u'微博图片爬取完毕，共%d张, 保存路径%s'%(image_count-1, image_path)
