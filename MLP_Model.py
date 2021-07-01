#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/4/8 19:07
# @Author :'liuyu'
# @Version：V 0.1
# @File : 
# @desc :
import torch
import torch.nn as nn
import torch.nn.functional as F

x_input = torch.randn(2,3,10)
print(x_input)

class MLP(nn.Module):
    def __init__(self,input_dim,hidden_dim, output_dim):
        super(MLP,self).__init__()

        self.fc1 = nn.Linear(input_dim,hidden_dim)
        self.fc2 = nn.Linear(hidden_dim,output_dim)

    def forward(self,inputs):
        intermediate = F.relu(self.fc1(inputs))
        outputs = self.fc2(intermediate)

        outputs = F.softmax(outputs,dim =2)

        return  outputs

model = MLP(10,20,5)
x_output = model(x_input)
print(x_output.shape)