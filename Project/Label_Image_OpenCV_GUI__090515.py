# -*- coding: utf-8 -*-
"""
Created on Sun Apr 09 21:19:50 2015

@author: Sarunya
"""
import cv2
import os
import numpy as np

WINDOW_NAME = "Label image"
#WINDOW2_NAME = "Temp"
all_img = []
class_img = []
rootdir = './dataset'
datadir = './Ldataset'
drawing = False # true if mouse is pressed
Cnow = None
ix,iy = -1,-1


def nothing(x):
    pass


# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,img,img2,Cnow
    sizeB = cv2.getTrackbarPos('Size',WINDOW_NAME)
    # color of class
    if Cnow == 0 :
	r = 0x17
	g = 0xbe
	b = 0xcf
    elif Cnow == 1 :
	r = 0xff
	g = 0x7f
	b = 0x0e
    elif Cnow == 2 :
	r = 0x2c
	g = 0x77
	b = 0xb4
    elif Cnow == 3 :
	r = 0x2c
	g = 0xa0
	b = 0x2c
    elif Cnow == 4 :
	r = 0xd6
	g = 0x67
	b = 0x28
    elif Cnow == 5 :
	r = 0x94
	g = 0x67
	b = 0xbd
    elif Cnow == 6 :
	r = 0x8c
	g = 0x56
	b = 0x4b
    elif Cnow == 7 :
	r = 0xe3
	g = 0x77
	b = 0xc2
    elif Cnow == 8 :
	r = 0x7f
	g = 0x7f
	b = 0x7f
    elif Cnow == 9 :
	r = 0xbc
	g = 0xbd
	b = 0x22
    else:
	print "please! select class number"
	r = 0xff
        g = 0xff
        b = 0xff

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True and Cnow != None:
            cv2.circle(img,(x,y),sizeB,(r,g,b),-1)
	    cv2.circle(img2,(x,y),sizeB,(r,g,b),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
	if Cnow != None:
            cv2.circle(img,(x,y),sizeB,(r,g,b),-1)
	    cv2.circle(img2,(x,y),sizeB,(r,g,b),-1)
    cv2.imshow(WINDOW_NAME,img)
    #cv2.imshow(WINDOW2_NAME,img2)



if __name__ == '__main__':    
    for root,dirs,files in os.walk(rootdir):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG'):
                all_img.append(f)
                temp = all_img.pop()
		img_name = os.path.basename(os.path.join(root,temp))
		
		print "--labeling image : " , img_name
		img = cv2.imread(os.path.join(root,temp),cv2.IMREAD_COLOR)
		img2 = cv2.imread(os.path.join(root,temp),cv2.IMREAD_GRAYSCALE)

		cv2.namedWindow(WINDOW_NAME)
                #cv2.namedWindow(WINDOW2_NAME)
                
                cv2.createTrackbar('Size',WINDOW_NAME,5,20, nothing)
		cv2.setMouseCallback(WINDOW_NAME,draw_circle)
		    	
		while(1):
                    cv2.imshow(WINDOW_NAME,img)
                    k = cv2.waitKey(0)
		    if k == ord('0'):
			print "class: 0"
			Cnow=0
		    elif k == ord('1'):
			print "class: 1"
			Cnow=1
		    elif k == ord('2'):
			print "class: 2"
			Cnow=2
		    elif k == ord('3'):
			print "class: 3"
			Cnow=3
		    elif k == ord('4'):
			print "class: 4"
			Cnow=4
		    elif k == ord('5'):
			print "class: 5"
			Cnow=5
		    elif k == ord('6'):
			print "class: 6"
			Cnow=6
		    elif k == ord('7'):
			print "class: 7"
			Cnow=7
		    elif k == ord('8'):
			print "class: 8"
			Cnow=8
		    elif k == ord('9'):
			print "class: 9"
			Cnow=9
	    	    elif k == 27: # wait for ESC key to exit
        	        cv2.destroyAllWindows()
        		print "you pressed esc"
			break
    		    elif k == ord('s'): # wait for 's' key to save and exit
			file_name = img_name.split(".")
			cv2.imwrite("_d"+file_name[0]+".bmp",img2)
        		cv2.destroyAllWindows()
    		        print "you pressed save "
			break        	        
			
		    
                #cv2.destroyAllWindows()
		Cnow = None
                
   
