# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 20:08:33 2020

@author: cm
"""


import re
import pandas as pd
import openpyxl
from openpyxl.styles import Font
import csv


def load_words(file):
    """
    Load a txt
    """

    with open(file, encoding='utf-8', errors='ignore') as fp:

        lines = fp.readlines()
        lines = [l.strip() for l in lines if l.strip() != '']

    return lines


def writer_excel(file, pre_words, datas):
    i = 1
    xls = openpyxl.Workbook()
    sheet = xls.active
    xls.get_sheet_by_name("Sheet")
    # sheet.title = sheetname
    foot = Font(name="等线", size=12)

    # sheet.cell.font = foot
    pre_counts = 0
    for data in datas:
        if data in pre_words:
            pre_counts += 1
            continue
        sheet.cell(i, 1, data).font = foot
        i += 1
    print(pre_counts)
    xls.save(file)


def writer_csv(file, pre_word, datas):
    f = open(file, 'w', encoding="utf-8", newline="")
    csv_writer = csv.writer(f)
    pre_counts = 0
    for data in datas:
        if data in pre_word:
            pre_counts += 1
            continue
        csv_writer.writerow([data])
    print(pre_counts)
    f.close()


def writer_txt(file, datas):
    f = open(file, 'w', encoding="utf-8")
    for d in datas:
        word = " ".join(d)
        f.write(word + "\n")
    f.close()


def writer_mergedata(file, datas):
    f = open(file, 'w', encoding="utf-8", newline="")
    csv_writer = csv.writer(f)
    for d in datas:
        csv_writer.writerow([d])
    f.close()


def writer_mergetxt(file, datas):
    f = open(file, 'w', encoding="utf-8")
    for d in datas:
        f.write(d + "\n")
    f.close()


def save_txt(file, lines):
    lines = [l+'\n' for l in lines]
    with open(file, 'w+', encoding='utf-8') as fp:      # a+添加
        fp.writelines(lines)
        print("Write data to file (%s) finished !"%file)




def sentence_split_regex(sentence):
    """
    Sentence segmentation
    """
    #print("3", sentence)
    if sentence is not None:
        sub_sentence = re.split(r"[.,！!？?;；]", sentence)     # 分句
        #print(1, sub_sentence)
        sub_sentence = [s for s in sub_sentence if s != '']
        # print(sub_sentence)
        # print(2, sub_sentence)
        if sub_sentence != []:
            return sub_sentence
        else:
            return []
    else:
        return []
    

def remove_characters_irregular(corpus):
    """
    Corpus: type string
    re,sub(pattern,repl,string) 把字符串中的所有匹配表达式pattern中的地方替换成repl
    [^**] 不匹配unicode字符集中的任何字符
    """
    corpus = re.sub(u"[^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a -\']+", "", corpus)
    return re.sub(r"[。,，！!？?;；\s…~～]+|\.{2,}|&hellip;+|&nbsp+|_n|_t", "", corpus)


def calcul_word_frequence(dic1, dic2):
    '''
    :param dic1:{'我':200,'喜欢':2000,....}:
    :param dic2:{'我':300,'你':1000,....}:
    :return:{'我':500,'喜欢':2000,'你':1000,....}
    '''
    keys = (dic1.keys()) | (dic2.keys())
    total = {}
    for key in keys:
        total[key] = dic1.get(key, 0) + dic2.get(key, 0)
    return total


def load_data(file, Header=0, Index_col=None, Sheet_name=None):
    """
    :param file: the path of excel
    :param Header: the first line of DataFrame (whether chose the first line of DataFrame as the index name)
    :param Index_col: the first column of DataFrame （whether chose the first column of DataFrame as the column name）
    :param Sheet_name: these sheet-names in the excel
    :return: a lot of sheets
    """
    dfs = pd.read_csv(file)
    # print(dfs[sheet_names[0]]['content'][1])

    return dfs



class ToolWord():
    """
    Remove some word special
    return: a word or ''
    """
    def remove_word_special(self, word):
        """
        # Word start with number and end with others: ['6氪','5亿美元','99美元']
        # Word start with not number and end with number: ['Q1']
        # Word is all numbers: ['199','16','25']
        # Word has "年","月" or "日": ['年1','年12月','月2','年9月','9年']
        # Word has "个","十","百","千","万","亿": ['500万','20万']
        # English word: ['Goog','Amaz','YouT']
        # Word has "你","我","他","她","它": ['如果你']
        """
        if not self.is_has_english(word) and \
            not self.is_has_number(word):
            return word
        else:
            return ''

    def is_all_number_list(self,words):
        return True if sum([self.is_all_number(word) for word in words]) == len(words) else False
                   
    @staticmethod
    def is_has_english(word):
        pattern = '[a-zA-Z]'
        result = ''.join(re.findall(pattern, word))
        return True if len(result) > 0 else False

    
    @staticmethod
    def is_has_number(word):
        pattern = '[0-9]'
        result = ''.join(re.findall(pattern,word))
        return True if len(result)>0 else False

    @staticmethod
    def is_all_number(word):
        pattern = '[0-9]'
        result = ''.join(re.findall(pattern,word))
        return True if result==word else False

    @staticmethod
    def is_english_word(word):
        pattern = '[a-zA-Z]'
        result = ''.join(re.findall(pattern,word))
        return True if result==word and len(word)>1 else False


            
 
if __name__ == '__main__':
    #
    rws = ToolWord()
    print(rws.is_all_number('23s2'))
    #
    words = ['2', '44', '3']
    print(rws.is_all_number_list(words))
    #
    words = '我们'
    print(rws.is_english_word(words))
    data = load_words("./data/stopword.txt")
    data.append('')
    print(data[-1], 1)

