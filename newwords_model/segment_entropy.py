# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 20:25:51 2020

@author: cm
"""



from .modules import get_scores
from .hyperparameters import Hyperparamters as hp
from .utils import sentence_split_regex, remove_characters_irregular
from .utils import load_data, load_words, writer_excel, writer_csv
import time
import sys

    
    
def get_words(corpus,
               top_k = hp.top_k,
               chunk_size = hp.chunk_size,
               min_n = hp.min_n,
               max_n = hp.max_n,
               min_freq = hp.min_freq):
    '''
    Word segmentation
    '''
    # Sentence segmentation and Clean characters irregulars
    if isinstance(corpus, str):
        corpus_splits = [remove_characters_irregular(sent) for sent in sentence_split_regex(corpus)]
    elif isinstance(corpus, list):
        #print(corpus)
        corpus_splits = [news for news in corpus if len(remove_characters_irregular(news)) != 0]     # 得到句子列表
        #print(corpus_splits)
    else:
        corpus_splits = remove_characters_irregular(corpus, chunk_size)
    # Get words and scores
    word_info_scores = get_scores(corpus_splits, min_n, max_n, chunk_size, min_freq)
    #print("word_info_scores", word_info_scores)
    # Sorted by score
    print(sorted(word_info_scores.items(), key=lambda item:item[1][-1], reverse=True)[top_k])
    new_words = [item[0] for item in sorted(word_info_scores.items(), key=lambda item:item[1][-1], reverse=True)]
    # Get the top k words

    if top_k > 1:
        new_words = [' '.join(l) for l in new_words[:top_k] if len(l) > 1]
    elif top_k < 1:           
        new_words = [' '.join(l) for l in new_words[:int(top_k*len(new_words))] if len(l) > 1]

    print(len(new_words))
    print(len(set(new_words)))
    return new_words
    
    
    
if __name__ == '__main__':
    ## 加载数据
    strat_time = time.time()
    f = sys.argv[1]
    contents = load_data(f).fillna('')['content'].tolist()
    #print(contents)
    print(len(contents))
    print(time.strftime("%Y%m%d_%H%M", time.localtime()))
    pre_words = load_words("./data/phrase.txt")
    #contents = ['23','dsad','dwq']
    print(len(pre_words))
    words = get_words(contents)
    data = time.strftime("%Y%m%d_%H%M", time.localtime())
    writer_csv("./data/new_word/" + sys.argv[2], pre_words, words)
    #writer_excel("./data/new_word/" + sys.argv[3], pre_words, words)
    end_time = time.time()
    print((end_time - strat_time) / 60)
    #print(words[:100])




    
    
    


