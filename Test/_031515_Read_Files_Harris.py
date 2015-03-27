# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 00:45:48 2015

@author: JD-SW
"""

from PIL import Image
import matplotlib.pylab as plt
import matplotlib.cm as cm
import numpy as np
import os
import cv2 as cv
from scipy.ndimage import filters
from pylab import *
rootdir = './dataset'

def compute_harris_response(im,sigma=1):
    """ Compute the Harris corner detector response function
        for each pixel in a graylevel image. """
    
    # derivatives
    imx = zeros(im.shape)
    filters.gaussian_filter(im, (sigma,sigma), (0,1), imx)
    imy = zeros(im.shape)
    filters.gaussian_filter(im, (sigma,sigma), (1,0), imy)
    
    # compute components of the Harris matrix
    Dxx = filters.gaussian_filter(imx*imx,sigma)
    Dxy = filters.gaussian_filter(imx*imy,sigma)
    Dyy = filters.gaussian_filter(imy*imy,sigma)
    
    # determinant and trace
    Ddet = Dxx*Dyy - Dxy**2
    Dtr = Dxx + Dyy
    
    return Ddet / Dtr
        
def get_harris_points(harrisim,min_dist=10,threshold=0.1):
    """ Return corners from a Harris response image
        min_dist is the minimum number of pixels separating
        corners and image boundary. """
        
    # find top corner candidates above a threshold
    corner_threshold = harrisim.max() * threshold
    harrisim_t = (harrisim > corner_threshold) * 1
    
    # get coordinates of candidates
    coords = array(harrisim_t.nonzero()).T
    
    # ...and their values
    candidate_values = [harrisim[c[0],c[1]] for c in coords]
    
    # sort candidates
    index = argsort(candidate_values)
    
    # store allowed point locations in array
    allowed_locations = zeros(harrisim.shape)
    allowed_locations[min_dist:- min_dist,min_dist:- min_dist] = 1
    
    # select the best points taking min_distance into account
    filtered_coords = []
    for i in index:
        if allowed_locations[coords[i,0],coords[i,1]] == 1:
            filtered_coords.append(coords[i])
            allowed_locations[(coords[i,0]-min_dist):(coords[i,0]+min_dist),
                              (coords[i,1]-min_dist):(coords[i,1]+min_dist)] = 0

    return filtered_coords
    
def plot_harris_points(image,filtered_coords):
    """ Plots corners found in image. """
    plt.figure()
    plt.gray()
    plt.imshow(image)
    plt.plot([p[1] for p in filtered_coords],[p[0] for p in filtered_coords],'*b')
    plt.axis('off')
    plt.show()

def readfiles():
    all_im=[]
    for root,dirs,files in os.walk(rootdir):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG'):
                im = Image.open(os.path.join(root,f)).convert('LA')
#                im = Image.open(os.path.join(root,f))
#                im = im.convert('LA')
                
                # save image
#                plt.imshow(im)
#                # Remove axes and ticks
#                plt.axis('off')
##        
#                plt.show()
#                plt.contour(l, [60, 211])
                all_im.append(np.asarray(im.getdata(),dtype=np.uint8))                
    return all_im
    
    


def main():
    all_im = readfiles()
#    img = PIL.Image.fromarray(arr)
#    fromarray
##
    
    for im in all_im:
#        img = PIL.Image.fromarray(im)
        harrisim = compute_harris_response(im)
        filtered_coords = get_harris_points(harrisim,5,.2)
        plot_harris_points(im, filtered_coords)
#        plt.imshow(img)
#                # Remove axes and ticks
#        plt.axis('off')
##        
#        plt.show()
    

    
#    filtered_coords = get_harris_points(harrisim,6)
    


if __name__ == '__main__':
    main()

