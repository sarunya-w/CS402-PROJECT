import cv2
import os
import numpy as np
import copy
import Image
from matplotlib import pyplot as plt
import cPickle
from scipy.ndimage import filters
import sys
import scipy.ndimage
sys.setrecursionlimit(10000)

if __name__=='__main__':
	img = np.array(Image.open('test.jpg').convert('L'))
	#print img
	#img2 = Image.open('test.jpg').convert("L")
	#print "---",img2
	freq = np.log(np.abs(np.fft.fft2(img)))
	fshift = np.log(np.abs(np.fft.fftshift(freq)))
	fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(14, 6))

	#fft_x = np.fft.fft2(img)
	#n = len(fft_x)
	#freq2 = np.fft.fftfreq(n, 1/f_s)
	#print n
	#print freq
	s=(100./freq.shape[0],100./freq.shape[1])
	print s
	e = scipy.ndimage.zoom(freq,s,order = 2)
	d = len(e)
	print d
	print scipy.ndimage.zoom(freq,s,order = 2)

	#f = np.fft.fft2(img)
	#fshift = np.fft.fftshift(freq)
	magnitude = 20*freq
	magnitude_spectrum = 20*fshift

	#or b in xrange(wd):
	#for rpin xrange(wd):


	ax[0,0].set_title('Input Image')
	ax[0,0].imshow(img, cmap = 'gray')
	ax[0,1].set_title('FFT')
	ax[0,1].imshow(freq, cmap = 'gray')
	ax[1,0].set_title('FFTshift')
	ax[1,0].imshow(magnitude_spectrum, cmap = 'gray')
	ax[1,1].set_title('resize:100')
	ax[1,1].imshow(e, cmap = 'gray')
	plt.show()
	
	freq
"""
	ax[0,0].hist(freq.ravel(), bins=100)
	ax[0,0].set_title('hist(freq)')
	ax[0,1].hist(np.log(freq).ravel(), bins=100)
	ax[0,1].set_title('Input Image')
	ax[1,0].imshow(img, cmap = 'gray')
	ax[1,0].set_title('log(freq)')
	ax[1,1].imshow(img, interpolation="none")
	plt.show()
	"""
