# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 16:48:08 2015

@author: Sarunya
"""
import os
import sys
import pickle
import numpy as np
import time
import random


##create clients
from IPython import parallel
c = parallel.Client(packer='pickle')
c.block = True
#print(c.ids)

##create direct view
dview = c.direct_view()
dview.block = True
#print len(dview)



#    global 
dsetname = './dataset'
ddesname = 'fft_dataset'
clmax = 11 #clmax is amount of class
theta_dim = 1
images_files = []
class_files = []
sampling = 20
dset = 1
#nofiles = 1

def timestamp(tt=time.time()):
    st=time.time()    
    print("    took: %.2f sec"%(st-tt))
    return st

if __name__ == '__main__':
    isTrain = True #train (test: False)
    for root, dirs, files in os.walk(dsetname):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG') or f.endswith('png') or f.endswith('PNG'):
                # read image to array (PIL) 
                images_files.append(os.path.join(root,f))
                
                img_name = os.path.basename(os.path.join(root,f))
                file_name = img_name.split(".")
                if isTrain is True:
                    # check image don't have file type 'bmp'
                    if os.path.isfile(os.path.join(root , 'bmp/' + file_name[0] + '.bmp')) == False:
                        print "plese label" , root , img_name
                        sys.exit()#break
                    else:
                        class_files.append(os.path.join(root , 'bmp/' + file_name[0] + '.bmp'))
    
    dsetname = dsetname.split("/")
    dview.execute("from fftengine import *")
    dview['images_files']=images_files
    dview['class_files']=class_files
    dview['isTrain']=isTrain
    dview['sampling']=sampling
    for i in xrange(dset):
        ts=time.time()
        dview.execute("vs ,cs = getVector(images_files,class_files,sampling,isTrain)")
        ts=timestamp(ts)
        vs=np.array(dview.gather('vs'),dtype=np.float32)
        cs=np.array(dview.gather('cs'))
        
        if cs[0] is None:
            cs = None
            
        if not os.path.exists(ddesname):
            os.makedirs(ddesname)
        if not os.path.exists(ddesname+'/'+dsetname[1] +'/'+ str(sampling)):
            os.makedirs(ddesname+'/'+dsetname[1] +'/'+ str(sampling))
        
        rfile = ddesname+'/' +dsetname[1] + '/'+ str(sampling) +'/'+ 'dataset%02d.pic'%(i)
        #rfile = ddesname+'/' +dsetname[1] + '/'+ 'dataset%02d.pic'%(i)

        pickleFile = open(rfile, 'wb')
        theta_range = vs.shape[1]
        size = vs.shape[0]
        samples = cs
        I = vs
        pickle.dump((clmax,theta_dim,theta_range,size,samples,I), pickleFile, pickle.HIGHEST_PROTOCOL)
        pickleFile.close()