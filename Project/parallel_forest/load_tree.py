# -*- coding: utf-8 -*-
"""
Created on Thu May 07 18:32:47 2015

@author: Sarunya
"""
import pickle
from sctree import tree
pickleFile = open('20150507_164012.pic', 'rb')
root = pickle.load(pickleFile)
pickleFile.close()

#init the test tree
t=tree()
t.settree(root)