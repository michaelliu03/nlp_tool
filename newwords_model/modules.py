# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 20:08:58 2020

@author: cm
"""


import math
import types
import collections
from operator import mul
from pygtrie import Trie
from functools import reduce
from .utils import calcul_word_frequence, load_words, writer_txt
from .probability import entropy_of_list
from .hyperparameters import Hyperparamters as hp
from .utils import ToolWord
from .tokenization import FullTokenizer


tokenizer = FullTokenizer.from_scratch(do_lower_case=True, spm_model_file=None)


def generate_ngram(corpus, n=2):
    """
    Generate the ngram word-group possible by token_length(2,3,4)
    return: generator (economize IO)
    """
    def generate_ngram_str(text, n):

        datas = tokenizer.tokenize(text)   # 分割句子，得到每个字
        for data in datas:
            for i in range(0, len(data)-n+1):
                yield data[i:i+n]

    if isinstance(corpus, str):    # 判断corpus的类型，字符串
        for ngram in generate_ngram_str(corpus, n):
            yield ngram
    elif isinstance(corpus, (list, types.GeneratorType)):
        for text in corpus:
            for ngram in generate_ngram_str(text, n):
                yield ngram


def get_ngram_frequence_infomation(corpus, max_n=4, chunk_size=10000000, min_freq=5):   # 统计ngrams的词频
    """
    Get words's frequences
    """
    ngram_freq_total = {}    # stock word frequence
    ngram_keys = {i: set() for i in range(1, max_n + 2)}      # ngram_keys={1:(); 2:(); 3:();...max_n + i:()}


    def get_frequence_chunk(corpus_chunk):
        """
        Get chunk's frequence
        Chunk: a part of Corpus
        """
        ngram_freq = {}
        for ni in range(1, max_n+2):    # 1 2 3 4 5
            ngram_generator = [tuple(l) for l in generate_ngram(corpus_chunk, ni)]
            nigram_freq = dict(collections.Counter(ngram_generator))      # 统计词出现的频率
            ngram_keys[ni] = (ngram_keys[ni] | nigram_freq.keys())     # 保留ngram包含的词
            ngram_freq = {**nigram_freq, **ngram_freq}

        ngram_freq = {word: count for word, count in ngram_freq.items() if count >= min_freq}    # 每个chunk的ngram频率统计

        return ngram_freq

    if isinstance(corpus, types.GeneratorType):
        for corpus_chunk in corpus:
            ngram_freq = get_frequence_chunk(corpus_chunk)
            ngram_freq_total = calcul_word_frequence(ngram_freq, ngram_freq_total)
    elif isinstance(corpus, list):
        len_corpus = len(corpus)  
        for i in range(0, len_corpus, chunk_size):
            corpus_chunk = corpus[i:min(len_corpus, i+chunk_size)]
            ngram_freq = get_frequence_chunk(corpus_chunk)
            ngram_freq_total = calcul_word_frequence(ngram_freq, ngram_freq_total)

    for k in ngram_keys:
        ngram_keys[k] = ngram_keys[k] & ngram_freq_total.keys()
    return ngram_freq_total,ngram_keys


def calcul_ngram_entropy(ngram_freq, ngram_keys, n):
    """
    Calcul entropy by ngram frequences
    """
    # Calcul ngram entropy

    if isinstance(n, collections.abc.Iterable):
        entropy = {}
        for ni in n:
            entropy = {**entropy, **calcul_ngram_entropy(ngram_freq, ngram_keys, ni)}
        return entropy
      
    ngram_entropy = {}
    parent_candidates = ngram_keys[n+1]    # 计算ngrams的左右熵时，获取n+1 gram的候选项

    if n != 1:
        target_ngrams = ngram_keys[n]
    else:
        print(4)
        target_ngrams = [l for l in ngram_keys[n] if ToolWord().is_english_word(l[0])]

    if hp.CPU_COUNT == 1:
        # Build trie for n+1 gram     构建字典树
        left_neighbors = Trie()
        right_neighbors = Trie()


        for parent_candidate in parent_candidates:
            # print(parent_candidate)   ('盈', '利', '模', '式')
            right_neighbors[parent_candidate] = ngram_freq[parent_candidate]
            # print(right_neighbors)    Trie(('盈', '利', '模', '式'): 6)
            left_neighbors[parent_candidate[1:]+(parent_candidate[0],)] = ngram_freq[parent_candidate]
            # print("left_neighbors", left_neighbors)  Trie(('利', '模', '式', '盈'): 6)

        # Calcul entropy
        for target_ngram in target_ngrams:
            try:  
                right_neighbor_counts = (right_neighbors.values(target_ngram))    # [12, 16, 3, 6, 9, 5, 5, 3, 5, 4, 4, 6, 11]
                right_entropy = entropy_of_list(right_neighbor_counts)      # 计算右信息熵
            except KeyError:
                right_entropy = 0
            try:
                left_neighbor_counts = (left_neighbors.values(target_ngram))
                left_entropy = entropy_of_list(left_neighbor_counts)
            except KeyError:
                left_entropy = 0
            ngram_entropy[target_ngram] = (left_entropy, right_entropy)
        return ngram_entropy
    else:
        # Multi process
        pass


def calcul_ngram_pmi(ngram_freq, ngram_keys, n):    # 计算凝聚度
    """
    # Pointwise Mutual Information 
    # Average Mutual Information
    """
    if isinstance(n, collections.abc.Iterable):
        mi = {}
        for ni in n:
            mi = {**mi, **calcul_ngram_pmi(ngram_freq,ngram_keys,ni)}
        return mi

    if n != 1:
        target_ngrams = ngram_keys[n]
    else:
        print(4)
        target_ngrams = [l for l in ngram_keys[n] if ToolWord().is_english_word(l[0])]       

    n1_totalcount = sum([ngram_freq[k] for k in ngram_keys[1] if k in ngram_freq])
    target_n_total_count = sum([ngram_freq[k] for k in ngram_keys[n] if k in ngram_freq])
    mi = {}
    for target_ngram in target_ngrams:
        target_ngrams_freq = ngram_freq[target_ngram]
        joint_proba = target_ngrams_freq/target_n_total_count
        indep_proba = reduce(mul, [ngram_freq[(char,)] for char in target_ngram])/((n1_totalcount)**n)
        pmi = math.log(joint_proba/indep_proba, hp.e)
        ami = pmi/len(target_ngram)                 
        mi[target_ngram] = (pmi, ami)
    return mi


def get_scores(corpus,     # list 或 string
               min_n=2,
               max_n=4,       # 最大ngram
               chunk_size=1000000,       # 每次读的数据块大小
               min_freq=5):      # 最小word的频次
    """
    Calcul the score of words
    :return: tuple with word
    """
    ngram_freq, ngram_keys = get_ngram_frequence_infomation(corpus, max_n, chunk_size, min_freq)
    print(1)
    # ngram_keys:   {1:{};2:{}...max_n+1: {})
    # ngram_freq:  {(word1,..wordn) : freq}
    # Get left and right ngram entropy
    left_right_entropy = calcul_ngram_entropy(ngram_freq, ngram_keys, range(min_n, max_n+1))
    print(2)
    # left_right_entropy):   {('klo',): (0, 0.0), ('twitter',): (0, 0), ...} key 词组包含的单词，value =（左信息熵，右信息熵)
    # Get pmi ngram entropy

    mi = calcul_ngram_pmi(ngram_freq, ngram_keys, range(min_n, max_n+1))
    print(3)
    # mi:    {('twitter',): (0.0, 0.0), ('galaxy',): (0.0, 0.0),...}   key词组包含的单词，value =（pmi，ami)
    # Join keys of entropy and keys of pmi
    joint_phrase = mi.keys() & left_right_entropy.keys()
    # print(joint_phrase)
    # Word liberalization
    w1 = 1
    w2 = 2.5
    word_liberalization = lambda el, er: math.log((el * hp.e ** er+0.00001)/(abs(el - er)+1), hp.e) \
                                       + math.log((er * hp.e ** el+0.00001)/(abs(el - er)+1), hp.e)

    word_info_scores = {word: (mi[word][0], mi[word][1], left_right_entropy[word][0], left_right_entropy[word][1],
                               min(left_right_entropy[word][0], left_right_entropy[word][1]),
                               w1 * word_liberalization(left_right_entropy[word][0], left_right_entropy[word][1]) + w2 * mi[word][1]
                               )
                        for word in joint_phrase if len(word) > 1}
    # (pmi, ami, letf, right, min(letf, right),  加权)


    target_ngrams = word_info_scores.keys()
    stopwords = load_words("./data/stopword.txt")
    rstopwords = load_words("./data/rstopword.txt")
    print(len(target_ngrams))
    print(len(set(target_ngrams)))
    stopwords.append('')
    invalid_target_ngrams = set([n for n in target_ngrams if (n[0] in stopwords or n[-1] in stopwords or n[-1] in rstopwords
                                                              or (n[0].isdigit() and n[-1].isdigit()))])


    for n in invalid_target_ngrams:
        word_info_scores.pop(n)

    return word_info_scores

