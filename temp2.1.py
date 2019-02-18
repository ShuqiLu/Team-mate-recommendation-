import numpy as np
from gensim import corpora, models, similarities
from pprint import pprint
import time
import jieba
def load_stopword():
    f_stop = open('停用词表.txt')
    sw = [line.strip() for line in f_stop]
    f_stop.close()
    return sw
def write_list(file_output,list_to_write):
    f=open(file_output,"w+",encoding='utf-8')

    for lists in list_to_write:
        for words in lists:
            f.write(words)
            f.write(' ')
        f.write('\n')
    f.close()
if __name__ == '__main__':

    t_start = time.time()
    stop_words = load_stopword()
    f = open('output.tsv',encoding='UTF-8')
    texts=[]
    '''
    texts2=[]
    #进行结巴分词，以及去停用词语料库初始处理
    for line in f:
        mytexts=line.split('\\n')
        for mytext in mytexts:
            wordlist=list(jieba.cut(mytext))
            real_wordlist=[]
            for word in wordlist:
                if word not in stop_words and word !='\n' and word !=' ' and word!='\t':
                    real_wordlist.append(word)
            if len(real_wordlist)>20:
                texts.append(real_wordlist)
                texts2.append(mytext)
    ''' 
    for line in f:
        mytexts=line.split(' ')
        wordlist=[]
        for word in mytexts :
            if word!='\n':
                wordlist.append(word)
        if(len(wordlist)>20):
            texts.append(wordlist)       
    f.close()
    #write_list('output.tsv',texts)
    #将文档按照段落分好，写入文件方便将这些文档归类到相应的主题
    '''
    k=0
    f=open('output2.tsv',"w+",encoding='utf-8')
    for paragraph in texts2:
        paragraph=paragraph.strip('\n')
        f.write(str(k))
        f.write('\t')
        f.write(paragraph)
        f.write('\n')
        k=k+1
    f.close()
    '''
    
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpus_tfidf = models.TfidfModel(corpus)[corpus]
    num_topics = 30
    lda = models.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=dictionary,
                            alpha=0.01, eta=0.01, minimum_probability=0.0001,
                            update_every = 1, chunksize = 100, passes = 1
                           )

    # 随机打印某10个文档的主题
    f=open('result3.tsv',"w+",encoding='utf-8')
    num_show_topic = 3  # 每个文档显示前几个主题
    print ('7.结果：10个文档的主题分布：--')
    doc_topics = lda.get_document_topics(corpus_tfidf)  # 所有文档的主题分布
    idx = np.arange(M)
    #np.random.shuffle(idx)
    #idx = idx[:10]
    for i in idx:
        topic = np.array(doc_topics[i])
        topic_distribute = np.array(topic[:, 1])
        topic_idx = topic_distribute.argsort()[:-num_show_topic-1:-1]
        f.write(str(i))
        f.write('\t')
        for item in topic_idx:
            f.write(str(item))
            f.write('\t')
        f.write('\n')
         
        print (('第%d个文档的前%d个主题：' % (i, num_show_topic)), topic_idx)
        print (topic_distribute[topic_idx])
    f.close()  

    num_show_term = 20 # 每个主题显示几个词
    print ('8.结果：每个主题的词分布：--',num_show_term )
    f=open('result4.tsv',"w+",encoding='utf-8')
    for topic_id in range(num_topics):
        print ('主题#%d：\t' % topic_id)
        term_distribute_all = lda.get_topic_terms(topicid=topic_id,topn=20)
        term_distribute = term_distribute_all[:20]
        term_distribute = np.array(term_distribute)
        term_id = term_distribute[:, 0].astype(np.int)
        print ('词：\t',)
        i=1
        for t in term_id:
            print (dictionary.id2token[t],end=" ")
            f.write(str(i))
            f.write('\t')
            f.write(dictionary.id2token[t])
            f.write('\t')
            f.write(str(term_distribute[:, 1][i-1]))
            f.write('\n')
            i=i+1
        f.write('\n')
        print ('\n概率：\t', term_distribute[:, 1])
    f.close()
        
        