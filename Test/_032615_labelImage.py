# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 00:45:48 2015

@author: JD-SW
"""

from PIL import Image
import matplotlib.pylab as plt
#import matplotlib.cm as cm
import numpy as np
import os

file_list=[]
class_img=[]
def nextImage():
    global file_list
    global class_img
    f=file_list.pop()
    im = Image.open(os.path.join(root,f))
    class_img = im.convert('LA')
    # save image
    #plt.imshow(im)
    plt.imshow(class_img)
    # Remove axes and ticks
    plt.axis('off')
#        
    plt.show()
    print "debug: nextImage():"+f
    
def onclick(event):
    global class_img
    global fig
    x=int(event.xdata)
    y=int(event.ydata)
    print x,", ", y
    pdata=class_img.load()
    pdata[x,y]=(0,255)
    #class_img.putpixel([x,y],255)
    fig.clf()
    plt.imshow(class_img)
    #plt.show()
    
def onpress(event):
    if event.key=='x':
        nextImage()
#    if event.key=='x':
#        nextImage()
        

#def readfiles():
#    all_im=[]
#    
#    for root,dirs,files in os.walk(rootdir):
#        for f in files:
#            if f.endswith('jpg') or f.endswith('JPG'):
#                im = Image.open(os.path.join(root,f))
#                im = im.convert('LA')
#                # save image
#                plt.imshow(im)
#                # Remove axes and ticks
#                plt.axis('off')
##        
#                plt.show()
#                fig.canvas.mpl_connect('key_press_event', press)
##                while ginput()!='x'
##                    print("clicked",x)
##                plt.contour(l, [60, 211])
#                all_im.append(np.asarray(im.getdata(),dtype=np.uint8))                
#    return all_im
    
if __name__ == "__main__":
    rootdir = 'dataset'
    fig=plt.figure()
    for root,dirs,files in os.walk(rootdir):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG'):   
                file_list.append(f)
    
    
    fig.canvas.mpl_connect('motion_notify_event', onclick)
    fig.canvas.mpl_connect('key_press_event', onpress)
    nextImage()
#    for root,dirs,files in os.walk(rootdir):
#        for f in files:
#            if f.endswith('jpg') or f.endswith('JPG'):
#                    im = Image.open(os.path.join(root,f))
#                    im = im.convert('LA')
#                    # save image
#                    plt.imshow(im)
#                    # Remove axes and ticks
#                    plt.axis('off')
#                #        
#                    plt.show()
                    #a=plt.ginput()
#                    pause=1
#                    while pause:
#                        pass
                    #a=plt.ginput()
                    #print ax
    #a = readfiles()
#    readfiles()
    


