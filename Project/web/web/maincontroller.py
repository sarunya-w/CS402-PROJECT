# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 16:48:08 2015

@author: Sarunya
"""


def maincontroller(images_files,class_files,sampling,isTrain):
    import numpy as np
    ##create clients
    from IPython import parallel
    c = parallel.Client(packer='pickle')
    c.block = True
    
    ##create direct view
    dview = c.direct_view()
    dview.block = True

    dview.execute("from fftengine import *")
    dview['images_files']=images_files
    dview['class_files']=class_files
    dview['isTrain']=isTrain
    dview['sampling']=sampling

    dview.execute("vs ,cs ,pos = getVector(images_files,class_files,sampling,isTrain)")
    vs=np.array(dview.gather('vs'),dtype=np.float32)
    cs=np.array(dview.gather('cs'))
    pos=dview.gather('pos')
        
    dview.abort()
    return vs , cs ,pos