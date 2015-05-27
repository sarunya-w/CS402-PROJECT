# -*- coding: utf-8 -*-
"""
Created on Thu May 07 18:17:14 2015

@author: Sarunya
"""
import pickle
pickleFile = open('fft_dataset/train(1)/dataset00.pic', 'rb')
clmax,theta_dim,theta_range,size,samples,I,pos = pickle.load(pickleFile)
pickleFile.close()