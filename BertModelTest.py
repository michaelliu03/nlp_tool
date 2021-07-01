#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/8 19:07
# @Author :'liuyu'
# @Version：V 0.1
# @File : 
# @desc :
import torch
import torch.nn as nn

from transformers import BertModel,BertTokenizer

sententce = 'i like eating apples very much'

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedder = BertModel.from_pretrained('bert-base-cased',output_hidden_states =True)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

    def forward(self,inputs):
        tokens = self.tokenizer.tokenize(inputs)
        print(tokens)
        tokens_id = self.tokenizer.convert_tokens_to_ids(tokens)
        print(tokens_id)
        #test = self.tokenizer.convert_ids_to_tokens(tokens_id)
        #print(test)
        tokens_id_tensor = torch.tensor(tokens_id).unsqueeze(0)
        outputs = self.embedder(tokens_id_tensor)
        print(outputs[0])

model =  Model()
results = model(sententce)