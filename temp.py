def save_html(url):
	global index
	seen_url.add(url)
	source = requests.get(url,headers=header,timeout=3,allow_redirects=True)
	html=source.content#.text
	if '.html' in url:
		#soup = BeautifulSoup(html,"html.parser",fromEncoding='gb2312')
		#title=soup.title
		#print(title)
		print('html: ',url)
		w.write(url+'\t'+str(index)+'\n')
		#data = soup.findAll(text=True)
		#data=filter(visible, data)
		#data=list(data)
		try:
			html=html.decode('gb2312')
			wt=open('/home/shuqi_lu/projects/dachuang/game_html/'+str(index),'w',encoding='utf-8')
			wt.write(html)
		except:
			wt=open('/home/shuqi_lu/projects/dachuang/game_html/'+str(index),'wb')
			wt.write(html)
		
		#for item in data:
			#print()
		#	item=item.replace('\t',' ')
		#	item=item.replace('\n',' ')
		#	item=item.replace('\r',' ')
		#	wt.write(item)
		index+=1
	else:
		try:
			html=html.decode('gb2312')
		except:
			html=''
		links=webpage_regex.findall(html)
		for urls in links:
			if url in seen_url or  url in no_url:
				continue
			if "http://www.godasai.com/" not in url:
				continue
			print('links: ',urls)
			save_html(urls)
			if index==10:
				print(seen_url)
				return
import requests
import re
import queue
#from bs4 import BeautifulSoup,Comment
url="http://www.godasai.com/"
#url="http://www.godasai.com/zhuanye/wenke/wenke/2016-08-24/821.html"
header={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6','referer':'link'}
user_agent='Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
w=open('game.txt','w')
no_url=['http://bbs.godasai.com/','http://www.godasai.com/wangzhangonggao/']#,'/e/config/','/d/','/e/class/','/e/data/','/e/enews/','/e/update/']
webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
seen_url=set()
def visible(element):
	if element.parent.name in ['script']:
		return False
	return True
def save_html(url):
	global index
	q = queue.Queue()
	q.put(url)
	while not q.empty():
		url=q.get()
		seen_url.add(url)
		source = requests.get(url,headers=header,timeout=3,allow_redirects=True)
		html=source.content#.text
		try:
			html=html.decode('gb2312')
		except:
			html=''
		links=webpage_regex.findall(html)
		for urls in links:
			if urls in seen_url or  urls in no_url:
				continue
			if "http://www.godasai.com/" not in urls:
				continue
			print('links: ',urls)
			if '.html' in urls:
				print('html: ',urls)
				w.write(urls+'\t'+str(index)+'\n')
				seen_url.add(urls)
				source = requests.get(urls,headers=header,timeout=3,allow_redirects=True)
				htmls=source.content#.text
				try:
					htmls=htmls.decode('gb2312')
					wt=open('/home/shuqi_lu/projects/dachuang/game_html/'+str(index),'w',encoding='utf-8')
					wt.write(htmls)
				except:
					wt=open('/home/shuqi_lu/projects/dachuang/game_html/'+str(index),'wb')
					wt.write(htmls)
				index+=1
			else:
				q.put(urls)
			if index==100:
				print(seen_url)
				return
def main():
	save_html(url)
if __name__ == '__main__':
	global index
	index=0
	main()



