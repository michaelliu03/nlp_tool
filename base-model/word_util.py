#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/8 19:07
# @Author :'liuyu'
# @Version：V 0.1
# @File : 
# @desc :

sentences = ["i like china"," i like apple"]
word_squence = ' '.join(sentences).split()
word_list = list(set(word_squence))
word_dict = {w:i for i,w in enumerate(word_list)}
print(word_squence)

skip_gram = []
for i in range(1,len(word_squence)-1):
    target = word_dict[word_squence[i]]
    print(target)
    content = [word_dict[word_squence[i-1]],word_dict[word_squence[i+1]]]

    for w in content:
        skip_gram.append([target,w])

print(skip_gram)