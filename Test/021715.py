# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 00:45:48 2015

@author: JD-SW
"""

from PIL import Image
import matplotlib.pylab as plt
import matplotlib.cm as cm
import numpy as np
import os
rootdir = 'dataset'
def readfiles():
    all_im=[]
    for root,dirs,files in os.walk(rootdir):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG'):
                im = Image.open(os.path.join(root,f))
                im = im.convert('LA')
                plt.imshow(im)
                # Remove axes and ticks
                plt.axis('off')
#        
                plt.show()
#                plt.contour(l, [60, 211])
                all_im.append(np.asarray(im.getdata(),dtype=np.uint8))                
    return all_im
    
if __name__ == "__main__":
    a = readfiles()
#    readfiles()
    print a


