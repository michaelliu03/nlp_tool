from utils import load_words, writer_mergedata
import sys
import time
import pandas as pd

def merge_data(data1, data2):
    '''
    word_dict = {}
    for word in data1:
        if word not in word_dict.keys():
            word_dict.setdefault(word, 1)
        else:
            word_dict[word] += 1

    for word in data2:
        if word not in word_dict.keys():
            word_dict.setdefault(word, 1)
        else:
            word_dict[word] += 1
    '''
    print(len(set(data1)))
    data = data1 + data2
    data = set(data)
    print(len(data))
    return data



data1 = []
data1 = load_words(sys.argv[1])
data2 = load_words(sys.argv[2])
#print(data1[:10])
#print(data2[:10])
word_dicts = merge_data(data1, data2)
#print(word_dicts)
data = time.strftime("%Y%m%d_%H%M%S", time.localtime())
writer_mergedata(sys.argv[1], word_dicts)
files = "." + sys.argv[1].split(".")[1] + ".xlsx"
print(files)
df = pd.DataFrame(word_dicts)
df.to_excel(files, encoding='utf8', header=False, index=False)

