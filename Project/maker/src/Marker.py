import cv2
import os
import numpy as np
import copy

WINDOW_NAME = "Label image"
#WINDOW2_NAME = "Class image"
all_img = []
rootdir = './dataset'
drawing = False # true if mouse is pressed
Cnow = -1
ix,iy = -1,-1
i = 0
type_name = ".bmp"
exit = 0


def nothing(x):
    pass

def draw_null(event,x,y,flags,param):
    pass

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,img,img2,Cnow
    sizeB = cv2.getTrackbarPos('Size',WINDOW_NAME)
    # color of class
    if Cnow == 0 :
        r = 0x17
        g = 0xbe
        b = 0xcf
    elif Cnow == 1 :
        r = 0xff
        g = 0x7f
        b = 0x0e
    elif Cnow == 2 :
        r = 0x2c
        g = 0x77
        b = 0xb4
    elif Cnow == 3 :
        r = 0x2c
        g = 0xa0
        b = 0x2c
    elif Cnow == 4 :
        r = 0xd6
        g = 0x67
        b = 0x28
    elif Cnow == 5 :
        r = 0x94
        g = 0x67
        b = 0xbd
    elif Cnow == 6 :
        r = 0x8c
        g = 0x56
        b = 0x4b
    elif Cnow == 7 :
        r = 0xe3
        g = 0x77
        b = 0xc2
    elif Cnow == 8 :
        r = 0x7f
        g = 0x7f
        b = 0x7f
    elif Cnow == 9 :
        r = 0xbc
        g = 0xbd
        b = 0x22
    elif Cnow == 10 :
        r = 0xff
        g = 0xff
        b = 0xff



    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True and Cnow != -1:
            cv2.circle(img,(x,y),sizeB, (r,g,b),-1)
            cv2.circle(img2 ,(x,y),sizeB,Cnow,-1)


    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if Cnow != -1:
            cv2.circle(img,(x,y),sizeB,(r,g,b),-1)
            cv2.circle(img2 ,(x,y),sizeB,Cnow,-1)
            
    
    cv2.imshow(WINDOW_NAME,img)
    #cv2.imshow(WINDOW2_NAME, img2 )

def draw_continue():
    global img,img2

    height, width = img2.shape

    for i in range(height):
        for j in range(width):
            Cnow = img2[i,j]
            if Cnow == 0 :
                img[i,j] = [0x17,0xbe,0xcf]
            elif Cnow == 1 :
                img[i,j] = [0xff,0x7f,0x0e]
            elif Cnow == 2 :
                img[i,j] = [0x2c,0x77,0xb4]
            elif Cnow == 3 :
                img[i,j] = [0x2c,0xa0,0x2c]
            elif Cnow == 4 :
                img[i,j] = [0xd6,0x67,0x28]
            elif Cnow == 5 :
                img[i,j] = [0x94,0x67,0xbd]
            elif Cnow == 6 :
                img[i,j] = [0x8c,0x56,0x4b]
            elif Cnow == 7 :
                img[i,j] = [0xe3,0x77,0xc2]
            elif Cnow == 8 :
                img[i,j] = [0x7f,0x7f,0x7f]
            elif Cnow == 9 :
                img[i,j] = [0xbc,0xbd,0x22]
            elif Cnow == 10 :
                img[i,j] = [0xff,0xff,0xff]


if __name__ == '__main__':    
    for root,dirs,files in os.walk(rootdir):
        for f in files:
            all_img.append(f)
            temp = all_img.pop()
            
            img_name = os.path.basename(os.path.join(root,temp))
            file_name = img_name.split(".")

            if type_name in img_name :
                pass
                #print "---", img_name, "does not label---\n"
            else:
                print "--- labeling image : ", img_name
                img = cv2.imread(os.path.join(root,temp),cv2.IMREAD_COLOR)
                
                #imgclone
                buffer_img = copy.copy(img)
                height, width = buffer_img.shape[:2]
    
                if os.path.isfile(os.path.join(root,file_name[0] + type_name)) == False:
                    img2 = np.zeros( (height,width), dtype=np.uint8)
                    img2[:] = [255]
                    #print "none"
                else:
                    img2 = cv2.imread(os.path.join(root,file_name[0] + type_name) ,cv2.IMREAD_GRAYSCALE) #img2 = cv2.imread(file_name[0] + type_name ,cv2.IMREAD_GRAYSCALE)
                    draw_continue()
                    #print "have" , type(img2)

                img_class = os.path.basename(os.path.join(root,temp))
                #print "--- labeling image : " , img_class

                cv2.namedWindow(WINDOW_NAME)
                #cv2.namedWindow(WINDOW2_NAME)


                cv2.createTrackbar('Size',WINDOW_NAME,5,20, nothing)
                cv2.setMouseCallback(WINDOW_NAME,draw_circle)
                #cv2.setMouseCallback(WINDOW2_NAME, draw_null)

                while(1):
                    cv2.imshow(WINDOW_NAME,img)
                    k = cv2.waitKey(0)
                    if k == ord('0'):
                        print "class: 0 - Oscillatoria sp."
                        Cnow = 0
                    elif k == ord('1'):
                        print "class: 1 - Chlorella sp."
                        Cnow = 1
                    elif k == ord('2'):
                        print "class: 2 - Closterium sp."
                        Cnow = 2
                    elif k == ord('3'):
                        print "class: 3 - Anabaena sp."
                        Cnow=3
                    elif k == ord('4'):
                        print "class: 4 - Melosira sp."
                        Cnow=4
                    elif k == ord('5'):
                        print "class: 5 - Cyclotella sp."
                        Cnow=5
                    elif k == ord('6'):
                        print "class: 6 - Actinastrum sp."
                        Cnow=6
                    elif k == ord('7'):
                        print "class: 7 - Ankistrodesmus sp."
                        Cnow=7
                    elif k == ord('8'):
                        print "class: 8 - Synedra sp."
                        Cnow=8
                    elif k == ord('9'):
                        print "class: 9 - Nitzschia sp."
                        Cnow=9 #case '-': cout<<"class null(256)"<<endl; Cnow=255; break;
                    elif k == ord('-'):
                        print " No class "
                        Cnow=10                 
                    elif k == ord('q'): # wait for ESC key to exit
                        cv2.destroyAllWindows()
                        break
                    elif k == ord('s'): # wait for 's' key to save and exit
                        file_name = img_name.split(".")
                        for root,dirs,files in os.walk(rootdir):
                            cv2.imwrite(os.path.join(root, file_name[0] + type_name) , img2 )
                            break
                        cv2.destroyAllWindows()
                        #"%02d"%(i)+ "_"+ 
                        print "you pressed save  " + file_name[0] + type_name + "  ( " + img_name + " )\n"
                        break
                    elif k == 27:
                        print "you pressed esc"
                        exit = 1
                        break

                Cnow = -1
                i = i+1
                if exit == 1:
                    break
