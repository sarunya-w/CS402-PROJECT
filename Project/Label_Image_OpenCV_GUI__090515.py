# -*- coding: utf-8 -*-
"""
Created on Sun Apr 09 21:19:50 2015

@author: Sarunya
"""

import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

WINDOW_NAME = "Label image"
WINDOW2_NAME = "Temp"
all_img=[]
class_img=[]
img=None
rootdir = './dataset'
sizeB=None
drawing = False # true if mouse is pressed
#mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1


def nothing(x):
    pass


# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,img
    sizeB = cv2.getTrackbarPos('Size',WINDOW_NAME)
    r = cv2.getTrackbarPos('R',WINDOW_NAME)
    g = cv2.getTrackbarPos('G',WINDOW_NAME)
    b = cv2.getTrackbarPos('B',WINDOW_NAME)
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img,(x,y),sizeB,(r,g,b),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(img,(x,y),sizeB,(r,g,b),-1)
    cv2.imshow(WINDOW_NAME,img)



if __name__ == '__main__':
    
    for root,dirs,files in os.walk(rootdir):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG'):
                all_img.append(f)
                test = all_img.pop()
		img = cv2.imread(os.path.join(root,test))

		cv2.namedWindow(WINDOW2_NAME)
                cv2.namedWindow(WINDOW_NAME)
                
                cv2.createTrackbar('Size',WINDOW_NAME,0,20, nothing)
     		cv2.createTrackbar('R',WINDOW_NAME,0,255,nothing)
                cv2.createTrackbar('G',WINDOW_NAME,0,255,nothing)
                cv2.createTrackbar('B',WINDOW_NAME,0,255,nothing)

		cv2.setMouseCallback(WINDOW_NAME,draw_circle)
		while(1):
                    h,w = img.shape[:2]
                    cv2.imshow(WINDOW_NAME,img)
                    k = cv2.waitKey(1) & 0xFF
                    
                    if k == ord('z'): # Zoom in, make image double size
                        img = cv2.pyrUp(img,dstsize = (2*w,2*h))
                    elif k == ord('a'):  # Zoom down, make image half the size
                        img = cv2.pyrDown(img,dstsize = (w/2,h/2))
                    elif k == 27:
                        break

                cv2.destroyAllWindows()
                
   
