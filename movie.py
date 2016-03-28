#coding=utf-8

import requests
import re
from gevent import monkey; monkey.patch_all()
import gevent
import gevent.pool
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def test(url):
	cookie = ''

	headers={'Referer': 'http://movie.douban.com', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2438.3 Safari/537.36', 'Host': 'movie.douban.com', 'Cookie': cookie}
	r = requests.get(url, headers=headers)
	if r.status_code == 200 :
		return headers

	return ''

def html(url): 
	'''
	返回网页内容
	'''
	return requests.get(url, headers=test(url)).text

def pages(url):
	'''
	返回每一页的地址
	'''
	pages = []

	count_rule = re.compile(r'<span class="count">\((.*?)\)</span>')
	count = count_rule.findall(html(url))
	try:
		count = int(count[0][1:-1]) #共*张 提取出中间的数字
	except:
		count = 40 #如果图片小于40张，只有一页，不出出现 共*张
	page = count/40

	if count%40 != 0:
		page += 1

	i = 0
	while i < page:
		n = i*40
		temp = '%s&start=%d&sortby=vote&size=a&subtype=a' % (url, n)
		pages.append(temp)
		i += 1

	return pages

def imgs(pages):
	'''
	获取所有图片地址
	'''
	imgs = []
	rule = re.compile(r'<img src="(http.*?)" />')
	for i in pages:
		img = rule.findall(html(i))
		imgs.extend([j.replace('photo/thumb', 'photo/raw') for j in img])

	return imgs

def download(urls):
	while len(urls):
		url = urls.pop()
		print '正在下载 %s' % url
		filename = url.split('/')[-1]
		r = requests.get(url, headers={'Referer':'http://movie.douban.com'}, stream=True)
		with open('./movie/'+filename, 'wb') as f:
			for chunk in r.iter_content(chunk_size=2048):
			# for chunk in r.iter_content():
				if chunk:
					f.write(chunk)
					f.flush()

def main(url):
	'''
	http://movie.douban.com/subject/6846893/photos?type=R

	下载海报 type=R
	下载壁纸 type=W
	下载剧照 type=S
	'''
	#print html(url)
	#print pages(url)
	#print imgs(pages(url))

	find_type = r'\?type=(\w)'
	type1 = re.findall(find_type, url)

	urlR = ''
	urlW = ''
	if type1[0] == 'R' :
		urlR = url
		urlW = url.replace('photos?type=R', 'photos?type=W')
	if type1[0] == 'W' :
		urlR = url.replace('photos?type=W', 'photos?type=R')
		urlW = url

	urls1 = imgs(pages(urlR))
	print '海报 %d张图片' % len(urls1)

	urls2 = imgs(pages(urlW))
	print '壁纸 %d张图片' % len(urls2)

	urls = urls1 + urls2
	p = gevent.pool.Pool(10)
	gevent.joinall([
		p.spawn(download, urls),
		p.spawn(download, urls),
		p.spawn(download, urls),
		p.spawn(download, urls),
		p.spawn(download, urls),
	])
	
		
	

if __name__ == '__main__':
	main(sys.argv[1])
	#print html(sys.argv[1])