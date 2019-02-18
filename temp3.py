#word2vecfrom gensim.models import Word2Vec
import gensim
import pickle
import re
import pickle
import os
import math
#记得要去掉停用词
def getCorpus():
	corpus=[]
	for row in range(0,100):
		row=str(row)
		f=open('/home/shuqi_lu/projects/dachuang/game_html/process'+row,'r',encoding='utf-8')
		content=f.read()
		#wordlist=list(jieba.cut(content))
		content=content.split('。')
		for item in content:
			corpus.append(item.split(' '))
	return corpus
def getWordModel(corpus):
	model=gensim.models.Word2Vec(corpus,min_count=1,size=200,workers=8)
	model.save('w2vquery_end.model')

	
if __name__ == '__main__':
	corpus=getCorpus()
	getWordModel(corpus)

