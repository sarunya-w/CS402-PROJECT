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
img=None
rootdir = './dataset'

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode,img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
            else:
                cv2.circle(img,(x,y),5,(0,0,255),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
        else:
            cv2.circle(img,(x,y),5,(0,0,255),-1)
    cv2.imshow('image',img)


def showImage():
    global all_img
    global class_img
    global mode
    global img
    f = all_img.pop()
    img = cv2.imread(os.path.join(root,f),cv2.IMREAD_GRAYSCALE)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_circle)

    while(1):
        cv2.imshow('image',img)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('m'):
            mode = not mode
            print mode
        elif k == 27:
            break

    cv2.destroyAllWindows()

        
    print "debug: nextImage():"+f

if __name__ == '__main__':
    
    for root,dirs,files in os.walk(rootdir):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG'):
                all_img.append(f)
                showImage()
                
   