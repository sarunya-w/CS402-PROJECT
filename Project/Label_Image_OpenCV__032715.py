# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 14:08:12 2015

@author: Sarunya
"""

import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

all_img=[]
class_img=[]

def showImage():
    global all_img
    global class_img
    f = all_img.pop()
    img = cv2.imread(os.path.join(root,f),cv2.IMREAD_GRAYSCALE)
#    img = cv2.IMREAD_GRAYSCALE(os.path.join(root,f))
#    img = Image.open()
#    class_img = img.convert('L')
    # save image
    #plt.imshow(im)
    cv2.imshow('image',img)
    k = cv2.waitKey(0) & 0xFF
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
        print "you pressed esc"
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('messigray.png',img)
        print "you pressed save"
    cv2.destroyAllWindows()
#    plt.imshow(class_img)
    # Remove axes and ticks
#    plt.axis('off')
#        
#    plt.show()
    print "debug: nextImage():"+f

if __name__ == '__main__':
    rootdir = './dataset'
    for root,dirs,files in os.walk(rootdir):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG'):
                all_img.append(f)
                showImage()