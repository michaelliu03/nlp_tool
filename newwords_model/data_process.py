#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/8 19:07
# @Author :'liuyu'
# @Version：V 0.1
# @File : 
# @desc :
import re

import pandas as pd
import unicodedata
import csv
import pandas
import sys
# This removes punctuation characters.

def writer_csv(file, datas):
    f = open(file, 'w', encoding="utf-8", newline="")
    csv_writer = csv.writer(f)
    for i in datas:
        w = i[0]
        v = i[1]
        if len(w.split(" ")) > 1:
            csv_writer.writerow([w, v])
    f.close()


def get_data(read_file, writer_file):
    f_r = open(read_file, 'r', encoding="utf-8")
    lines = f_r.readlines()
    i = 0
    datas = []
    for line in lines:
        temp = re.sub(r"[\@\~\`\$\^\"\]\[\n\^\*\(\)\=\+]", "", line)
        if temp.isspace() or len(temp.replace(" ", "")) <= 1:
            continue
        #rint(type(temp))
        temp = temp.lstrip(" ")
        if len(temp) == 0:
            continue
        i += 1
        if i % 1000000 == 0:
            print(i)


        datas.append(temp)

    print(len(datas))
    df = pd.DataFrame(datas, columns=['content'])
    f_r.close()
    print(1)
    df.to_csv(writer_file)

get_data(sys.argv[1], sys.argv[2])