#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/8 19:07
# @Author :'liuyu'
# @Version：V 0.1
# @File : 
# @desc :
import pandas as pd
import jieba
import  matplotlib.pyplot  as plt
from wordcloud import WordCloud#词云包
from gensim import corpora, models, similarities
import gensim


def getStopWords():
    stopwords = pd.read_csv("D:\BaiduNetdiskDownload\qiyue-online\shenduxuexi\data\stopwords.txt", index_col=False,
                            quoting=3, sep="\t", names=['stopword'], encoding='utf-8')
    return stopwords


def Word2Cloud():
    df = pd.read_csv("D:\BaiduNetdiskDownload\qiyue-online\shenduxuexi\data\sports_news.csv", encoding='utf-8')
    df = df.dropna()
    content = df.content.values.tolist()
    #rint(content)
    segment =[]
    for line in content:
        try:
            segs = jieba.lcut(line)
            for seg in segs:
                if len(seg) > 1 and seg !='\r\n':
                    segment.append(seg)
        except:
            print(line)
            continue
    #print(segment)
    plt.rcParams['figure.figsize'] = (10.0,8.0)
    words_df = pd.DataFrame({'segment':segment})
    stopwords = getStopWords()#pd.read_csv("D:\BaiduNetdiskDownload\qiyue-online\shenduxuexi\data\stopwords.txt",index_col = False, quoting = 3, sep='\t',names=['stopword'], encoding='utf-8')
    #words_df = stopwords['stopword'].values
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
    #words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
    words_stat=words_df.groupby(by=['segment'])['segment'].agg([("计数","count")])
    words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
    #words_stat.head()
    print(words_stat.head(5))
    wordcloud = WordCloud(font_path="D:\self_prj_new\nlp_tool\data\simhei.ttf", background_color="white", max_font_size=80)
    word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}
    wordcloud = wordcloud.fit_words(word_frequence)
    plt.imshow(wordcloud)




def LdaModel():
    print("...LdaModel...")
    stopwords = getStopWords()
    df = pd.read_csv("D:/BaiduNetdiskDownload/qiyue-online/shenduxuexi/data/technology_news.csv", encoding='utf-8')
    df = df.dropna()
    #print(df)
    lines = df.content.values.tolist()
    sectences = []
    for line in lines:
        try:
            segs = jieba.lcut(line)
            segs = list(filter(lambda x:len(x) > 1 and x not in stopwords, segs))
            #segs = filter(lambda x:len(x)>1, segs)
            #segs = filter(lambda x:x not in stopwords, segs)
            sectences.append(segs)
        except:
            print(line)
            continue
    #print(sectences)

    dictionary = corpora.Dictionary(sectences)
    #print(dictionary)
    corpus = [dictionary.doc2bow(sentence) for sentence in sectences]
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)
    print(lda.print_topic(3, topn=5))
    #print(corpus)

    # for word in sectences[5]:
    #     print(word)

    for topic in lda.print_topics(num_topics=20, num_words=8):
        print(topic[1])




if __name__ =='__main__':
    Word2Cloud()
    #LdaModel()