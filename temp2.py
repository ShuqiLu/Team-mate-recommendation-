#LDA
import codecs
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim import corpora, models, similarities
import jieba
from bs4 import BeautifulSoup,Comment
import jieba
def visible(element):
	if element.parent.name in ['script','ul','a'] or (element.parent.parent!=None and element.parent.parent.name in ['script','ul','a']):
		return False
	return True
def ReadWeb():
	#f_in=open('game.txt','r').readlines()
	#for row in f_in:
	#	row=row.strip().split('\t')[1]
	for row in range(0,100):
		row=str(row)
		try:
			print(row)
			f=open('/home/shuqi_lu/projects/dachuang/game_html/'+row,'r',encoding='utf-8')
			html=f.read()
		except:
			print('error: ',row)
			f=open('/home/shuqi_lu/projects/dachuang/game_html/'+row,'rb')
			html=f.read().decode('gb2312','ignore')
		soup = BeautifulSoup(html,"html.parser")#,fromEncoding='utf-8')
		data = soup.findAll(text=True)
		data=filter(visible, data)
		data=list(data)
		s=''
		for item in data:
			item=str(item)
			#print(type(item))
			if item=='\n' or item=='\r' or item=='\r\n':
				continue
			a=item.replace('\t',' ').replace(' ','').replace('\r','').replace('\n',' ')
			#print(a,'----',a)
			s+=a
		wordlist=list(jieba.cut(s))
		w=open('/home/shuqi_lu/projects/dachuang/game_html/process'+row,'w',encoding='utf-8')
		for word in wordlist:
			w.write(word+' ')

def LdaAnalysis():
	train = []
	stopword = open('stopwords.txt','r',encoding='utf-8').readlines()
	stopwords = [ w.strip() for w in stopword ]
	#for row in f_in:
	#	row=row.strip().split('\t')[1]
	for row in range(0,100):
		row=str(row)
		f=open('/home/shuqi_lu/projects/dachuang/game_html/process'+row,'r',encoding='utf-8')
		content=f.read()
		#wordlist=list(jieba.cut(content))
		content=content.split(' ')
		train.append([ w for w in content if w not in stopwords ])
	dictionary = Dictionary(train)
	corpus = [ dictionary.doc2bow(text) for text in train ]
	print('data load ok...')
	#lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=30)
	#lda.save('lda.model')
	
	num_topics = 50
	corpus_tfidf = models.TfidfModel(corpus)[corpus]
	#lda = models.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=dictionary, alpha=0.01, eta=0.01, minimum_probability=0.0001, update_every = 1, chunksize = 100, passes = 1 )
	#lda.save('lda.model')
	

	lda = LdaModel.load('lda.model')
	#print(lda.print_topics(30))
	#lda.print_topic(20)
	
	#test_doc = list(jieba.cut(test_doc))　　  #新文档进行分词
	#doc_bow = dictionary.doc2bow(test_doc)      #文档转换成bow
	doc_bow=corpus[0]
	doc_lda = lda[doc_bow]               #得到新文档的主题分布
	#doc_lda=lda.get_document_topics(corpus_tfidf[0])
	print (doc_lda)
	doc_lda.sort(key=lambda x:x[1],reverse=True)
	for topic in doc_lda:
		print ("%s\t%f\n"%(lda.print_topic(topic[0]), topic[1]))
	print(len(doc_lda))

def main():
	#ReadWeb()
	LdaAnalysis()

if __name__ == '__main__':
	main()
	
