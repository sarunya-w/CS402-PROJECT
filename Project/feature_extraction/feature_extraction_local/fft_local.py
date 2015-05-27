# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 17:31:34 2015

@author: Sarunya
"""
import os
import sys
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import scipy.ndimage
import pickle
#from scipy.ndimage import filters
import time
import random

sys.setrecursionlimit(10000)
bs = 200
wd = 8 # theta_range=wd*wd*2
clmax = 11 #clmax is amount of class
theta_dim = 1
dset = 1


def timestamp(tt=time.time()):
    st=time.time()    
    print("    took: %.2f sec"%(st-tt))
    return st
  
def normFFT(images_file):
    # apply to array
    img = np.array(images_file)
    #converte image to frequency domain
    #t=np.log(np.abs(np.fft.fftshift(np.fft.fft2(img))))
    f = np.log(np.abs(np.fft.fft2(img)))

    """    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

    ax1.axis('off')
    ax1.imshow(img, cmap=plt.cm.gray)
    ax1.set_title('Input image')

    # Rescale histogram for better display
    #hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))

    ax2.axis('off')
    ax2.imshow(f, cmap=plt.cm.gray)
    ax2.set_title('Fast Furior Tranform')
    plt.show()
    """
    #scaling
    s=(100./f.shape[0],100./f.shape[1])
    #normalized frequency domian
    return scipy.ndimage.zoom(f,s,order = 2)

def getValue(images):
    f = normFFT(images) #f=[100,100]
    rmax,cmax = f.shape
    
    sg = np.zeros((2*wd,wd)) #sg[60,30]
    sg[0:wd,:]=np.log(np.abs(f[rmax-wd:rmax,0:wd])) #sg[0:30,:] = f[70:100,0:30]
    sg[wd:2*wd,:]=np.log(np.abs(f[0:wd,0:wd])) #sg[30:60,:] = f[0:30,0:30]
    
    return sg.reshape(-1)
    

def getVector(images_files,class_files,samples,isTrain):
    ts=time.time()
    sub_img = []
    sub_cs = []
    bb = bs//2
    pos = []
    
    for f in xrange(len(images_files)):
        img = Image.open(images_files[f]).convert('L')
        imgx = np.array(img)
    #converte image to frequency domain
        fd=np.log(np.abs(np.fft.fftshift(np.fft.fft2(imgx))))
        f = np.log(np.abs(np.fft.fft2(imgx)))
        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(14, 6))
    
        ax[0,0].set_title('FFT')
        ax[0,0].imshow(f, cmap = 'gray')
        ax[0,1].set_title('sg')
        ax[0,1].imshow(fd, cmap = 'gray')

        ax[1,1].set_title('input image')
        ax[1,1].imshow(imgx, cmap = 'gray')
    
        plt.show()        
        
        w , h = img.size
        pixels=[]
        #print '%02d %s'%(f,images_files[f])
        for i in xrange(samples):
            r = np.random.randint(bb, h-bb)
            c = np.random.randint(bb, w-bb)
            pixels.append((c,r))
            #if isTrain==False:
            #    pos.append((c,r))
            box = (c-bb, r-bb, c + bb, r + bb)
            output_img = img.crop(box)
            sub_img.append(getValue(output_img))
    
        if isTrain:
            cimg = Image.open(class_files[f]).convert('L')
            for p in pixels:   
                sub_cs.append(cimg.getpixel(p))
        
    if isTrain:
        sub_img=np.array(sub_img,dtype=np.float32)
        sub_cs=np.array(sub_cs,dtype=np.uint32)
        sub_cs[sub_cs==255] = clmax - 1
    else:
        #sub_img=np.array(sub_img,dtype=np.float32)
        sub_cs=None       
    ts=timestamp(ts)

    return (sub_img ,sub_cs)


if __name__ == '__main__':
    isTrain = True #train (test: False)
    dsetname = './dataset'
    ddesname = 'fft_dataset'
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
        #C = pos
        pickle.dump((clmax,theta_dim,theta_range,size,samples,I), pickleFile, pickle.HIGHEST_PROTOCOL)
        pickleFile.close()
    