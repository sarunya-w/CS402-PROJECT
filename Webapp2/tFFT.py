# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 14:19:50 2015

@author: Sarunya
"""
import os
import sys
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import scipy.ndimage
from scipy.ndimage import filters
import pickle
import random

sys.setrecursionlimit(10000)

bs = 100 #bs is border size in sub_file
wd = 20 #wd-theta_range is level of the dimention vector
clmax = 11 #clmax is amount of class
theta_dim = 1

def normFFT(im_file):
    # apply to array
    img = np.array(im_file)
    #converte image to frequency domain
    #f=np.log(np.abs(np.fft.fftshift(np.fft.fft2(im))))
    f = np.log(np.abs(np.fft.fft2(img)))
    #scaling
    s=(100./f.shape[0],100./f.shape[1])
    
    #normalized frequency domian
    return scipy.ndimage.zoom(f,s,order = 2)

    
def G(x,mu,s):
    return 1.0/ np.sqrt(2.0*np.pi)*np.exp(((x-mu)**2)/(-2.0*s**2))


def getVector(im_file,wd):
    f = normFFT(im_file) #f=[100,100]
    rmax,cmax = f.shape 

    sg = np.zeros((2*wd,wd)) #sg[60,30]
    sg[0:wd,:]=np.log(np.abs(f[rmax-wd:rmax,0:wd])) #sg[0:30,:] = f[70:100,0:30]
    sg[wd:2*wd,:]=np.log(np.abs(f[0:wd,0:wd])) #sg[30:60,:] = f[0:30,0:30]
    

    """fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(14, 6))

    ax[0,0].set_title('FFT')
    ax[0,0].imshow(f, cmap = 'gray')
    ax[0,1].set_title('sg')
    ax[0,1].imshow(sg, cmap = 'gray')
    ax[1,0].set_title('fd')
    ax[1,0].imshow(fd, cmap = 'gray')
    ax[1,1].set_title('input image')
    ax[1,1].imshow(im_file, cmap = 'gray')

    plt.show()
    
    fd = np.zeros((wd,wd*2))
    fd[:,0:wd] = np.log(np.abs(f[0:wd,cmax-wd:cmax]))
    fd[:,wd:wd*2]=np.log(np.abs(f[0:wd,0:wd]))

    filters.gaussian_filter(fd, (3,3), (0,0), fd)

    fsgs=np.zeros(wd) #fsg[30]
    for b in xrange(wd): #b in 30
        for r in xrange(wd): # r in 30
            for c in xrange(wd): # c in 30
                rad=np.sqrt(r**2+c**2)            
                fsgs[b]=fsgs[b]+fd[r,c+wd]*G(rad,float(b),0.2)+fd[r,wd-c]*G(rad,float(b),0.2)
        fsgs[b]=fsgs[b]/(np.pi*float(b+1.0))
        fsgs=fsgs/np.linalg.norm(fsgs)
        fsgs.astype(np.float32)
    #print fsgs
    return fsgs
    """

    filters.gaussian_filter(sg, (3,3), (0,0), sg)
   
    fsg=np.zeros(wd)
    for b in xrange(wd):
        for r in xrange(wd):
            for c in xrange(wd):
                rad=np.sqrt(r**2+c**2)            
                fsg[b]=fsg[b]+sg[wd+r,c]*G(rad,float(b),0.2)+sg[wd-r,c]*G(rad,float(b),0.2)
        fsg[b]=fsg[b]/(np.pi*float(b+1.0))
        fsg=fsg/np.linalg.norm(fsg)
        fsg.astype(np.float32)
    return fsg


def crop_image(im_file,cs_file,samples,wd,mode):
    sub_img = []
    sub_cs = []
    img = Image.open(im_file).convert('L')
    w , h = img.size
    bb = bs//2
    if mode == 0: #train
    	cs = Image.open(cs_file).convert('L')
    	for i in xrange(samples):
    		r = np.random.randint(bb, h-bb)
    		c = np.random.randint(bb, w-bb)

    		box = (c-bb, r-bb, c + bb, r + bb)
    		output_img = img.crop(box)

    		sub_img.append(getVector(output_img,wd))
    		sub_cs.append(cs.getpixel((c,r)))

    else: #test
    	cs = np.zeros((h,w), dtype=np.uint8)
    	cs[:] = [0]

    	for r in xrange(bb,h-bb,bs):
    		for c in xrange(bb,w-bb,bs):
    			box = (c-bb, r-bb, c + bb, r + bb)
    			output_img = img.crop(box)

    			sub_img.append(getVector(output_img,wd))
    			sub_cs.append(0)
    			print "(r,c):(%d,%d)"%(r,c)

    return sub_img, sub_cs

def test(rfile,ddesname,dset,dfiles,samples,wd,mode):
    all_images = []
    all_class = []
    file_name = rfile.split(".")

    if file_name[1] == 'jpg' or 'JPG' or 'png' or 'PNG':
        all_images.append(rfile)
        k=0
        for i in range (dset):
            sub_images = []
            sub_class = []
            sub_img = []
            sub_cs = []

            xfile = all_images.pop()
            print '%02d-%d %s'%(i,k,xfile)

            sub_images , sub_class = crop_image(xfile,None,0,wd,mode)
            V = np.array(sub_images,dtype=np.float32)
            C = np.array(sub_class,dtype=np.uint32)
            #C[C==0] = None
            print ";;;", V , len(V)
            print "-----",  len(C)
            if not os.path.exists(ddesname):
                os.makedirs(dsetname)
            rfile = ddesname +'/'+ 'datasetTest%02d.pic'%(k)
            pickleFile = open(rfile, 'wb')
            pickle.dump((clmax,theta_dim,wd,len(C),C,V), pickleFile, pickle.HIGHEST_PROTOCOL)
            pickleFile.close()
            k=k+1
    else:
        print "File format not support"
        

def train(dsetname,ddesname,dset,dfiles,samples,wd,mode):
    all_images = []
    all_class = []
    cross = -1
    for root, dirs, files in os.walk(dsetname):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG') or f.endswith('png') or f.endswith('PNG'):
                # read image to array (PIL) 
                all_images.append(os.path.join(root,f))

                img_name = os.path.basename(os.path.join(root,f))
                file_name = img_name.split(".")

                # check image don't have file type 'bmp'
                if os.path.isfile(os.path.join(root , 'bmp/' + file_name[0] + '.bmp')) == False:
                    print "plese label" , root , img_name
                    cross = 1
                else:
                    all_class.append(os.path.join(root , 'bmp/' + file_name[0] + '.bmp'))

    k=0
    for i in range (dset):
        xarray = [] # list of sub files(img,class)
        sub_images = []
        sub_class = []
        sub_img = []
        sub_cs = []

        xarray = random.sample(zip(all_images,all_class), dfiles)
        for j in range (len(xarray)):
            if cross == 1:
                break

            xfiles = xarray.pop()
            print '%02d-%d %s'%(i,j,xfiles[0])
            sub_img , sub_cs = crop_image(xfiles[0],xfiles[1],samples,wd,mode)

            for x in xrange(samples) :
                sub_images.append(sub_img.pop())
                sub_class.append(sub_cs.pop())

        V = np.array(sub_images,dtype=np.float32)
        C = np.array(sub_class,dtype=np.uint32)
        C[C==255] = clmax - 1
        
        if not os.path.exists(ddesname):
            os.makedirs(dsetname)
        rfile = ddesname +'/'+ 'dataset%02d.pic'%(k)
        pickleFile = open(rfile, 'wb')
        pickle.dump((clmax,theta_dim,wd,len(C),C,V), pickleFile, pickle.HIGHEST_PROTOCOL)
        #print ";;;", V , len(V)
        #print "-----",C,  len(C)
        pickleFile.close()
        k=k+1


if __name__ == '__main__': #(dsetname,ddesname,dset,dfiles,samples,wd,mode)
    if len(sys.argv) < 2:
        #rfile = train('dataset','dataset_fft',4,100,10,20,0)
        rfile = test('[150413_111153]_01.jpg','dataset_fft',1,1,None,20,1)
        
    elif len(sys.argv) == 2:
        rfile = train(sys.argv[1])
        #t,dset=recall(sys.argv[1],rfile)
