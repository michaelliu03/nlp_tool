#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/8 19:07
# @Author :'liuyu'
# @Version：V 0.1
# @File : 
# @desc :

import numpy as np
import pandas as pd
import jieba
import random
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

def GetCorpus():
    print("<<<<GetCorpus>>>")
    df_sports = pd.read_csv("D:/BaiduNetdiskDownload/qiyue-online/shenduxuexi/data/sports_news.csv", encoding='utf-8')
    df_sports = df_sports.dropna()

    df_technology = pd.read_csv("D:/BaiduNetdiskDownload/qiyue-online/shenduxuexi/data/technology_news.csv", encoding='utf-8')
    df_technology = df_technology.dropna()

    df_car = pd.read_csv("D:/BaiduNetdiskDownload/qiyue-online/shenduxuexi/data/car_news.csv", encoding='utf-8')
    df_car = df_car.dropna()

    df_entertainment = pd.read_csv("D:/BaiduNetdiskDownload/qiyue-online/shenduxuexi/data/entertainment_news.csv", encoding='utf-8')
    df_entertainment = df_entertainment.dropna()

    df_military = pd.read_csv("D:/BaiduNetdiskDownload/qiyue-online/shenduxuexi/data/military_news.csv", encoding='utf-8')
    df_military = df_military.dropna()

    technology = df_technology.content.values.tolist()[1000:21000]
    car = df_car.content.values.tolist()[1000:21000]
    entertainment = df_entertainment.content.values.tolist()[:20000]
    military = df_military.content.values.tolist()[:20000]
    sports = df_sports.content.values.tolist()[:20000]

    #print(technology[5])
    return technology, car,entertainment, military,sports

def GetStopWords():
    stopwords = pd.read_csv("D:/BaiduNetdiskDownload/qiyue-online/shenduxuexi/data/stopwords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'],
                            encoding='utf-8')
    stopwords = stopwords['stopword'].values
    return stopwords


def preprocess_text(content_lines, sentences, category):
    for line in content_lines:
        try:
            segs=jieba.lcut(line)
            segs = filter(lambda x:len(x)>1, segs)
            segs = filter(lambda x:x not in stopwords, segs)
            sentences.append("__label__"+str(category)+" , "+" ".join(segs))
        except Exception:
            print (line)
            continue

def process_text():
    sentences = []
    technology, car, entertainment, military, sports = GetCorpus()
    preprocess_text(technology, sentences, 'technology')
    preprocess_text(car, sentences, 'car')
    preprocess_text(entertainment, sentences, 'entertainment')
    preprocess_text(military, sentences, 'military')
    preprocess_text(sports, sentences, 'sports')

    sentences_ = random.shuffle(sentences)
    print("writing data to fasttext format...")
    out = open('train_data.txt', 'w')
    for sentence in sentences:
        out.write(sentence + "\n")
    print("done!")



if __name__ =='__main__':
    print("...begin......")
    #print(car[3])
    stopwords = GetStopWords()
