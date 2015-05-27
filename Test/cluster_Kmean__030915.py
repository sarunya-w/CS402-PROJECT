# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 05:04:23 2015

@author: Sarunya Werasena
"""
from PIL import Image
import cv2
import numpy as np
from scipy.cluster.vq import *
import cPickle
import os
rootdir = 'dataset'

def harris_response(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.01*dst.max()]=[255,0,0]

#    cv2.imshow('dst',img)
#    if cv2.waitKey(0) & 0xff == 27:
#        cv2.destroyAllWindows()

#def kmean_cluster():
#    class1 = 1.5 * np.random.randn(100,2)
#    class2 = np.random.randn(100,2) + np.array( [ 5,5] )
#    features = np.vstack((class1,class2))
#    centroids,variance = kmeans(features,2)
#    code,distance = vq(features,centroids)
#
#    plt.figure()
#    ndx = np.where(code==0) [ 0]
#    plt.plot(features[ ndx,0] ,features[ ndx,1] , '*' )
#    ndx = np.where(code==1) [ 0]
#    plt.plot(features[ ndx,0] ,features[ ndx,1] , 'r.' )
#    plt.plot(centroids[ : ,0] ,centroids[ : ,1] , 'go' )
#    plt.axis('off')
#    plt.show()

def readfiles():
    all_im=[]
    for root,dirs,files in os.walk(rootdir):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG'):
                im = Image.open(os.path.join(root,f))
                im = im.convert('LA')
                
                # save image
                plt.imshow(im)
                # Remove axes and ticks
                plt.axis('off')
#        
                plt.show()
#                plt.contour(l, [60, 211])
                all_im.append(np.asarray(im.getdata(),dtype=np.uint8))                
    return all_im
    
def kmean_cluster(imlist):
    # get list of images
#    imlist = imtools.get_imlist('selected_fontimages/')
    imnbr = len(imlist)
    # load model file
#    with open('a_pca_modes.pkl','rb' ) as f:
    immean = pickle.load(open('a_pca_modes.pkl','rb' ))
    V = pickle.load(f)
    # create matrix to store all flattened images
    immatrix = np.array([np.array(Image.open(im)).flatten() for im in imlist] , 'f' )
        # project on the 40 first PCs
    immean = immean.flatten()
    projected = np.array( [np.dot(V[ :40] ,immatrix[i] - immean) for i in range(imnbr) ] )
            # k- means
    projected = np.whiten(projected)
    centroids,distortion = kmeans(projected,4)
    code,distance = vq(projected,centroids)

# plot clusters
    for k in range(4) :
        ind = where(code==k) [ 0]
        plt.figure()
        
        plt.gray()
        for i in range(minimum( len(ind),40)) :
            plt.subplot(4,10,i+1)
            plt.imshow(immatrix[ ind[ i] ] . reshape((25,25)))
            plt.axis('off')
            plt.show()
            
def main():
    img = cv2.imread('test.jpg')
    harris_response(img)
    a = readfiles()
    kmean_cluster(a)
    

if __name__ == '__main__':
    main()