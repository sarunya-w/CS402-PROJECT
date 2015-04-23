# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 14:19:50 2015

@author: Sarunya
"""

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import os
from scipy.spatial import kdtree
import cPickle
from scipy.ndimage import filters
import sys
import scipy.ndimage
sys.setrecursionlimit(10000)


#wd is level of the detail between 10 to 50
wd=20
rootdir = './dataset'
target = 'bmp/'
all_files = []
all_class = []
all_im = []
i = 0
type_name = ".bmp"
bs = 100
samples = 10

def normFFT(im_file):
    img = np.array(im_file)
    #converte image to frequency domain
    #f=np.log(np.abs(np.fft.fftshift(np.fft.fft2(im))))
    f = np.log(np.abs(np.fft.fft2(img)))

    #scaling
    s=(100./f.shape[0],100./f.shape[1])
    #print s 

    #normalized frequency domian
    return scipy.ndimage.zoom(f,s,order = 2)

    
def G(x,mu,s):
    return 1.0/ np.sqrt(2.0*np.pi)*np.exp(((x-mu)**2)/(-2.0*s**2))


def getVector(im_file):
    f = normFFT(im_file) #f=[100,100]
    #print np.log(np.abs(f))
    rmax,cmax = f.shape 
    #print rmax , cmax

    #fd = np.zeros((wd,wd*2))
    sg = np.zeros((2*wd,wd)) #sg[60,30]
    #fd[:,0:wd] = np.log(np.abs(f[0:wd,cmax-wd:cmax]))
    sg[0:wd,:]=np.log(np.abs(f[rmax-wd:rmax,0:wd])) #sg[0:30,:] = f[70:100,0:30]
    #print sg
    #print len(sg)
    sg[wd:2*wd,:]=np.log(np.abs(f[0:wd,0:wd])) #sg[30:60,:] = f[0:30,0:30]
    #fd[:,wd:wd*2]=np.log(np.abs(f[0:wd,0:wd]))

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
   # filters.gaussian_filter(fd, (3,3), (0,0), fd)

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



def crop_image(imgfile,cfile):
    sub_img = []
    sub_c = []
    img = Image.open(imgfile).convert('L')
    c_img = Image.open(cfile).convert('L')
    w , h = img.size
    for i in xrange(samples):    	
        rmax = np.random.randint(0, h-bs)
        cmax = np.random.randint(0, w-bs)
        box = (cmax, rmax, cmax + bs, rmax + bs)
        output_img = img.crop(box)
        outC = c_img.crop(box)

        u = getVector(output_img)
        sub_img.append(u)
        
        pixels = outC.load()
        for x in range(bs/2):
            for y in range(bs/2):
                output_class = pixels[x, y]    
        sub_c.append(output_class)
    
    return sub_img, sub_c



if __name__ == '__main__':
    # read image to array   
    all_files= []
    all_class = []
    cross = -1
    for root, dirs, files in os.walk(rootdir):
        for f in files:
                if f.endswith('jpg') or f.endswith('JPG') or f.endswith('png') or f.endswith('PNG'):
                    all_files.append(os.path.join(root,f))

                    img_name = os.path.basename(os.path.join(root,f))
                    file_name = img_name.split(".")
                    if os.path.isfile(os.path.join(root,target + file_name[0] + type_name)) == False:
                        print "plese label" , root,img_name
                        cross = 1
                    else:
                        all_class.append(os.path.join(root,target + file_name[0] + type_name))


    j=0;
    end=0
    while end is not 1:
        sub_files = []
        sub_class = []
        sub_img = []
        sub_c = []

        for i in xrange(2000):
            if len(all_files) is 0:
                end=1         
                break
            if cross == 1:
            	end=1         
                break
            f = all_files.pop(0)
            c = all_class.pop(0)
              
            print '%02d %s'%(i,f)

            sub_img , sub_c = crop_image(f,c)
            #print sub_img
            #print sub_c
            for x in xrange(samples) :
            	temp1 = sub_img.pop()
            	temp2 = sub_c.pop()
            	sub_files.append(temp1)
            	sub_class.append(temp2)
            	#print '%02d %s'%(x,temp1)
            	#print '%02d %s'%(x,temp2)
            
            #sub_temp1.append(sub_img)
            #sub_temp2.append(sub_c)
            #print '%02d %s'%(i,sub_img) , "----"
            #print '%02d %s'%(i,sub_c)
            #print '%02d %s'%(i,sub_temp1)
            #print '%02d %s'%(i,sub_temp2)
            #temp = np.array(sub_c.pop())
            #print q
            #w = np.array(sub_c)
            #print sub_sclass
            #sub_files.append(sub_temp1) 
            #temp = sub_im.pop(0)
            #tempC = np.array(sub_c.pop())
            #sub_class.append(sub_temp2)
            #print sub_class
            #sub_bsg.append(sub_class)
     
        print '%02d %s'%(i,sub_files)
        print '%02d %s'%(i,sub_class)
        print "------------------\n"
        print '%02d %s'%(i,sub_files.pop())
        print '%02d %s'%(i,sub_class.pop())

        pickleFile = open('%s/fft%02d.dat'%(rootdir,j), 'wb')
        cPickle.dump((sub_class,sub_files), pickleFile, cPickle.HIGHEST_PROTOCOL)
        #tree = kdtree.KDTree(sub_bsg)
        #pickleFile = open('%s/tree%02d.dat'%(rootdir,j), 'wb')
        #cPickle.dump((sub_files,tree,wd), pickleFile, cPickle.HIGHEST_PROTOCOL)
        pickleFile.close()
        j=j+1
    ####load tree
#    pickleFile = open('%s/tree%02d.dat'%(rootdir,0), 'rb')
#    (all_files,tree,wd) = cPickle.load(pickleFile)
#    pickleFile.close()
#    findall(tree,all_files)

