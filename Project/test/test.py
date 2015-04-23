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

rootdir = './dataset'
if __name__ == '__main__':
    # read image to array   
    all_files= []
    all_class = []
    cross = -1
    for root, dirs, files in os.walk(rootdir):
        for f in files:
                if f.endswith('dat'):
                    filess = open(f,'r')
                    object_file = pickle.load(filess)

                  