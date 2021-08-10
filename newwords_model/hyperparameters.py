# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 19:31:35 2020

@author: cm
"""


import os
import math
pwd = os.path.dirname(os.path.abspath(__file__))


class Hyperparamters:
    # Parameters
    top_k = 1500
    chunk_size = 1000000
    min_n = 2 #1#2
    max_n = 4 
    min_freq = 5
    
    #
    e = math.exp(1)

    # CPU number used
    CPU_COUNT = 1 
    #

