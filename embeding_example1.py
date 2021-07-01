#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/8 19:07
# @Author :'liuyu'
# @Version：V 0.1
# @File : 
# @desc :
from torch import nn
import torch
import jieba
import numpy as np

raw_txt = """你好，北京，我爱你"""
words = list(jieba.cut(raw_txt))
print(words)
