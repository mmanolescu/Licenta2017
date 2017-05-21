
import stream_client as sc
import color_gradient_selector as cgs
import cv2
import os
import numpy as np

TMP_FILE = 'tmp.jpg'
OUT_FILE = 'out-1.jpg'

if __name__ == "__main__":
    index = 0
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
    while True:
        index = index + 1
        img = sc.get_next_jpeg()

        #os.remove(TMP_FILE)
        f = open(TMP_FILE, 'wb')
        f.write(img)
        f.close()

        imgFile = cv2.imread(TMP_FILE)
        imgFile1 = cgs.select_rgb_white_yellow(imgFile)

        res = np.concatenate((imgFile, imgFile1), axis=1)

        '''
        cv2.imshow('image', imgFile)
        cv2.waitKey(0)
        cv2.imshow('image', imgFile1)
        cv2.waitKey(0)
        '''

        cv2.imshow('image', res)
        cv2.waitKey(1)

        #cv2.imwrite(OUT_FILE, res)
        #out.write(res)

