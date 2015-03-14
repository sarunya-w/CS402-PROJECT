####TestOpenCV

import cv2
def main():
    windowname = "Hello OpenCV"
    img = cv2.imread("test.jpg") # your photo path
    cv2.imshow(windowname,img)
    cv2.waitKey(0)
    cv2.destroyWindow(windowname)
    pass

if __name__ == '__main__':
    main()