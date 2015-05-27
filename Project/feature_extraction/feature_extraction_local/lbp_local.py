# -*- coding: utf-8 -*-
"""
Created on Fri May 01 22:02:45 2015

@author: Sarunya
"""

import os
import sys
import numpy as np
from PIL import Image
import math
import pickle
import time
import scipy.ndimage
import random
import numpy as np
import matplotlib
from PIL import Image
from matplotlib import pyplot as plt
import scipy.ndimage
import skimage.feature as ft
from skimage import data
from skimage import data, color, exposure


sys.setrecursionlimit(10000)
bs = 200
wd = 8 # theta_range=wd*wd*2
clmax = 11 #clmax is amount of class
theta_dim = 1
dset = 1
#nofiles = 500

def timestamp(tt=time.time()):
    st=time.time()    
    print("    took: %.2f sec"%(st-tt))
    return st

def normLBP(images_file):
    METHOD = 'uniform'
    R = 2 #radius
    P = 8 #n_points
    img = np.array(images_file)
    f = ft.local_binary_pattern(img, P, R, METHOD)
    print f 
    return f

def getValue(images):
    f = normLBP(images)
    
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
    ddesname = 'lbp_dataset'
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
    for i in xrange(1):
        vs ,cs = getVector(images_files,class_files,1,isTrain)
        vs = np.array(vs,dtype=np.float32)
        #cs=np.array(cs)
        
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