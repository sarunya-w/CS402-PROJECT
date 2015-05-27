# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 14:19:50 2015

@author: Sarunya
"""

import os
import sys
import numpy as np
from PIL import Image
import scipy.ndimage
import pickle
from skimage.feature import hog
from skimage import data, color, exposure
import scipy.ndimage
import time
from cv2 import HOGDescriptor
import random
from matplotlib import pyplot as plt

sys.setrecursionlimit(10000)
bs = 200
wd = 8 # theta_range=wd*wd*2
clmax = 11 #clmax is amount of class
theta_dim = 1
dset = 1
nofiles = 1

def timestamp(tt=time.time()):
    st=time.time()    
    print("    took: %.2f sec"%(st-tt))
    return st

def normHOG(images_file):
    img = np.array(images_file)
    width, height = img.shape
    # SKIMAGE
    #fd , f = hog(img, orientations=8, pixels_per_cell=(height//8, width//8), cells_per_block=(16, 16), visualise=True)
    f = hog(img, normalise=True,pixels_per_cell=(height//4, width//4))
    print f.shape
    #print len(f)
   
    
    #scaling
    #s = (100./f.shape[0],100./f.shape[1])
    #normalized histogram of gradient
    return f#scipy.ndimage.zoom(f,s,order = 2)

def getValue(images):
    f = normHOG(images)
    #print f.shape 
    #rmax,cmax = f.shape
    #print f.shape
    #sg = np.zeros((2*wd,wd)) #sg[60,30]
    #sg[0:wd,:]=np.log(np.abs(f[rmax-wd:rmax,0:wd])) #sg[0:30,:] = f[70:100,0:30]
    #sg[wd:2*wd,:]=np.log(np.abs(f[0:wd,0:wd])) #sg[30:60,:] = f[0:30,0:30]
    
   # a = 
    #print a,len(a)
    return f.reshape(-1)

def getVector(images_files,class_files,samples,isTrain):
    ts=time.time()
    sub_img = []
    sub_cs = []
    bb = bs//2
    
    for f in xrange(len(images_files)):
        img = Image.open(images_files[f]).convert('L')
        w , h = img.size
        pixels=[]
        #print '%02d %s'%(f,images_files[f])
        for i in xrange(samples):
            r = np.random.randint(bb, h-bb)
            c = np.random.randint(bb, w-bb)
            pixels.append((c,r))
            box = (c-bb, r-bb, c + bb, r + bb)
            output_img = img.crop(box)
            sub_img.append(getValue(output_img))
    
        if isTrain:
            cimg = Image.open(class_files[f]).convert('L')
            for p in pixels:   
                sub_cs.append(cimg.getpixel(p))
    if isTrain == True:
        sub_img=np.array(sub_img,dtype=np.float32)
        sub_cs=np.array(sub_cs,dtype=np.uint32)
        sub_cs[sub_cs==255]= clmax - 1
    else:
        sub_cs=None       
    ts=timestamp(ts)

    return (sub_img ,sub_cs)


if __name__ == '__main__':
    isTrain = True #train (test: False)
    dsetname = './dataset'
    ddesname = 'hog_dataset'
    images_files = []
    class_files = []
    for root, dirs, files in os.walk(dsetname):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG') or f.endswith('png') or f.endswith('PNG'):
                # read image to array (PIL) 
                images_files.append(os.path.join(root,f))
                
                img_name = os.path.basename(os.path.join(root,f))
                file_name = img_name.split(".")
                # check image don't have file type 'bmp'
                if isTrain is True:
                    # check image don't have file type 'bmp'
                    if os.path.isfile(os.path.join(root , 'bmp/' + file_name[0] + '.bmp')) == False:
                        print "plese label" ,  img_name
                        sys.exit()#break
                    else:
                        class_files.append(os.path.join(root , 'bmp/' + file_name[0] + '.bmp'))
    
    #if isTrain is True:
    #    xarray = random.sample(zip( images_files,class_files), nofiles)  
    #    images_files = [a[0] for a in xarray]
    #    class_files = [a[1] for a in xarray]
    dsetname = dsetname.split("/")
    for i in xrange(dset):
        vs ,cs = getVector(images_files,class_files,1000,isTrain)
        vs = np.array(vs,dtype=np.float32)
        #cs=np.array(cs)500
        
        #if cs[0] is None:
        #    cs = None

        if not os.path.exists(ddesname):
            os.makedirs(ddesname)
        if not os.path.exists(ddesname+'/'+dsetname[1]):
            os.makedirs(ddesname+'/'+dsetname[1])
        #if not os.path.exists(ddesname+'/'+dsetname[1]+'/'+'100'):
        #    os.makedirs(ddesname+'/'+dsetname[1]+'/'+'100')

        #rfile = ddesname+'/' +dsetname[1] + '/'+ '100' +'/'+ 'dataset%02d.pic'%(i)
        rfile = ddesname+'/' +dsetname[1] + '/'+ 'dataset%02d.pic'%(i)

        pickleFile = open(rfile, 'wb')
        theta_range = vs.shape[1]
        size = vs.shape[0]
        samples = cs
        I = vs
        pickle.dump((clmax,theta_dim,theta_range,size,samples,I), pickleFile, pickle.HIGHEST_PROTOCOL)
        pickleFile.close()
        i = i+1