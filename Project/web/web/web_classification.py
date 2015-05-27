# -*- coding: utf-8 -*-
"""
Created on Thu May 07 17:06:11 2015

@author: Sarunya
"""
import os
import sys
sys.path
sys.path.append('../parallel_forest/')
from PIL import Image
from matplotlib import pyplot as plt
from scmain import recall,log
from maincontroller import *
import pickle
import numpy as np


#images_files = ["../parallel_forest/test/test.jpg"]
def display():
    mylog=log("test.log")
    t,dset=recall('../parallel_forest/dataset_pickle','../parallel_forest/20150510_022955.pic',mylog)
    dset.show()
    coordinate = []
    #img = Image.open(images_files).convert('L')
    #plt.imshow(img, cmap=plt.cm.gray)
    for i in range(len(dset.samples)):
        if dset.getL(i) != 10:
            print dset.getL(i) , dset.pos[i][0],dset.pos[i][1]

            coordinate.append( (dset.pos[i][0],dset.pos[i][1],dset.getL(i)))
            #print dset.getL(i)
            #print dset.pos[i][0]
            
            #plt.hold(True)
            #plt.text(dset.pos[i][0],dset.pos[i][1],dset.getL(i))
    print coordinate
    return coordinate

def gen_dataset(images_files):
    rfile="../parallel_forest/training/dataset00.pic"
    clmax = 11 #clmax is amount of class
    theta_dim = 1

    vs ,cs, pos = maincontroller(images_files,None,100,False)
#    vs = np.array(vs,dtype=np.float32)
    if cs[0] is None:
        cs = None
    
    pickleFile = open(rfile, 'wb')
    theta_range = vs.shape[1]
    size = vs.shape[0]
    samples = cs
    I = vs
    pickle.dump((clmax,theta_dim,theta_range,size,samples,I,pos), pickleFile, pickle.HIGHEST_PROTOCOL)
    pickleFile.close()


def master(filename):
    #mylog=log("test.log")
    images_files = []

    for root, dirs, files in os.walk('./static/uploads'):
        for f in files:
            if os.path.basename(os.path.join(root,f)) == filename:
                images_files.append(os.path.join(root,f))
                print os.path.join(root,f)
    print images_files           
    gen_dataset(images_files)
    cx = display()
#    #print cx
#    string = ""
    # for j in xrange(len(cx)):
    #     if cx[j][2] == 0 :
    #         color = "#cfbe17"
    #     elif cx[j][2] == 1 :
    #         color = "#0e7fff"
    #     elif cx[j][2] == 2 :
    #         color = "#b4772c"
    #     elif cx[j][2] == 3 :
    #         color = "#2ca02c"
    #     elif cx[j][2] == 4 :
    #         color = "#2867d6"
    #     elif cx[j][2] == 5 :
    #         color = "#bd6794"
    #     elif cx[j][2] == 6 :
    #         color = "#4b568c"
    #     elif cx[j][2] == 7 :
    #         color = "#c277e3"
    #     elif cx[j][2] == 8 :
    #         color = "#7f7f7f"
    #     elif cx[j][2] == 9 :
    #         color = "#22bdbc"
    # for j in xrange(len(cx)):
    #     if cx[j][2] == 0 :
    #         cx[j][2] = "#cfbe17"
    #     elif cx[j][2] == 1 :
    #         cx[j][2] = "#0e7fff"
    #     elif cx[j][2] == 2 :
    #         cx[j][2] = "#b4772c"
    #     elif cx[j][2] == 3 :
    #         cx[j][2] = "#2ca02c"
    #     elif cx[j][2] == 4 :
    #         cx[j][2] = "#2867d6"
    #     elif cx[j][2] == 5 :
    #         cx[j][2] = "#bd6794"
    #     elif cx[j][2] == 6 :
    #         cx[j][2] = "#4b568c"
    #     elif cx[j][2] == 7 :
    #         cx[j][2] = "#c277e3"
    #     elif cx[j][2] == 8 :
    #         cx[j][2] = "#7f7f7f"
    #     elif cx[j][2] == 9 :
    #         cx[j][2] = "#22bdbc"
#
#        #string = string + Markup('''<rect x="''' + "%d"%cx[j][0] + '''" y="''' + "%d"%cx[j][1] + '''" width="50" height="50" style="stroke:"''' + "%s"%color + '''";stroke-width:5;fill-opacity:0.1;stroke-opacity:0.9"/>''')
#        #string = string + "<rect x=" + "%d"%cx[j][0] + " y=" + "%d"%cx[j][1] + " width="50" height="50" style= \"" + "stroke:" + "%s"%color + ";stroke-width:5;fill-opacity:0.1;stroke-opacity:0.9\""/>"

    return cx

if __name__ == '__main__':
    mylog=log("test.log")
    #print "aaaaaaaaaaaaaaaaaa"
    master('test.jpg')
    # if len(sys.argv) < 2:
    #     mylog=log("test.log")
    #     images_files = ["../parallel_forest/test/test.jpg"]
    #     #print images_files
    #     #gen_dataset(images_files)
    #     cx = display()
        #return cx

    # elif len(sys.argv) == 2:
    #     mylog=log("test.log")
    #     images_files = ['./static/uploads/%s'%sys.argv[1]]
    #     #print images_files
    #     gen_dataset(images_files)
    #     display()