#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules
import time

import stream_client as sc
import color_gradient_selector as cgs
import cv2
import os
import numpy as np
import math

HOST = '192.168.100.17'    # Server(Raspberry Pi) IP address
PORT = 21567
ADDR = (HOST, PORT)
CENTER_INDEX = 320

TMP_FILE = 'tmp.jpg'


def separate_floor_from_obstacles():
    global last_good_index
    img = sc.get_next_jpeg()

    #os.remove(TMP_FILE)
    f = open(TMP_FILE, 'wb')
    f.write(img)
    f.close()

    imgFile = cv2.imread(TMP_FILE, cv2.CV_LOAD_IMAGE_COLOR)
    half_img = cv2.resize(imgFile, (0,0), fx=0.5, fy=0.5)
    hsv = cv2.cvtColor(half_img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(half_img, cv2.COLOR_BGR2GRAY)

    h, s, v = cv2.split(hsv)

    height, width = gray.shape
    print height, width
    D = width / 25

    gray = half_img

    obstaclePos = []
    for index in range(D, width - D, D):
        obstaclePos.append(0)
        #cv2.rectangle(gray, (index, height - D), (index + D, height - 1), (255, 0, 0), 3)
        floor = gray[(height - D):height, index:(index + D), : ]

        mean_valueR = floor[:, :, 0].mean()
        mean_valueG = floor[:, :, 1].mean()
        mean_valueB = floor[:, :, 2].mean()
        print mean_valueR, mean_valueG, mean_valueB

        for k in range(2, 7):
            #cv2.rectangle(gray, (index, height - k*D), (index + D, height - - (k - 1) * D), (255, 0, 0), 3)
            rect = gray[(height - k*D):(height - (k - 1) * D), index:(index + D), : ]

            mR = rect[:, :, 0].mean()
            mG = rect[:, :, 1].mean()
            mB = rect[:, :, 2].mean()
            print "------", mR, mG, mB, "-----", abs(mR - mean_valueR), abs(mG - mean_valueG), abs(mB - mean_valueB)

            #cv2.rectangle(gray, (index, height - k * D), (index + D, height - k * D - D), (255, 0, 0), 3)
            s = 15
            if abs(mR - mean_valueR) > s or abs(mG - mean_valueG) > s or abs(mB - mean_valueB) > s:
                print '----', k
                #cv2.rectangle(half_img, (index, height - k * D), (index + D, height - (k + 1) * D), (255, 0, 0), 3)
                obstaclePos[len(obstaclePos) - 1] = height - k * D
                break


    offset = D
    for pos in obstaclePos:
        cv2.rectangle(half_img, (offset, pos), (offset + D, pos), (255, 0, 0), 3)
        offset = offset + D

    #gray = cv2.cvtColor(half_img, cv2.COLOR_BGR2GRAY)
    #half_img =  cv2.Canny(gray, 230, 250)
    cv2.imshow('image', gray)
    cv2.waitKey(1)

    return None

def CheckGround():

    StepSize = 6
    EdgeArray = []

    orig_img = sc.get_next_jpeg()

    #os.remove(TMP_FILE)
    f = open(TMP_FILE, 'wb')
    f.write(orig_img)
    f.close()

    imgFile = cv2.imread(TMP_FILE, cv2.CV_LOAD_IMAGE_COLOR)
    img = cv2.resize(imgFile, (0,0), fx=0.5, fy=0.5)

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #convert img to grayscale and store result in imgGray
    imgGray = cv2.bilateralFilter(imgGray,9,30,30) #blur the image slightly to remove noise
    imgEdge = cv2.Canny(imgGray, 10, 50)             #edge detection

    # cv2.imshow("camera", imgEdge)
    # cv2.waitKey(0)

    imagewidth = imgEdge.shape[1] - 1
    imageheight = imgEdge.shape[0] - 1

    for j in range (0,imagewidth,StepSize):    #for the width of image array
        for i in range(imageheight-5,0,-1):    #step through every pixel in height of array from bottom to top
                                               #Ignore first couple of pixels as may trigger due to undistort
            if imgEdge.item(i,j) >= 100:       #check to see if the pixel is white which indicates an edge has been found
                EdgeArray.append((j,i))        #if it is, add x,y coordinates to ObstacleArray
                break                          #if white pixel is found, skip rest of pixels in column
        else:                                  #no white pixel found
            EdgeArray.append((j,0))            #if nothing found, assume no obstacle. Set pixel position way off the screen to indicate
                                               #no obstacle detected


    for x in range (len(EdgeArray)-1):      #draw lines between points in ObstacleArray
        cv2.line(img, EdgeArray[x], EdgeArray[x+1],(0,255,0),1)
    for x in range (len(EdgeArray)):        #draw lines from bottom of the screen to points in ObstacleArray
        cv2.line(img, (x*StepSize,imageheight), EdgeArray[x],(0,255,0),1)


    cv2.imshow("camera", img)
    cv2.waitKey(10)

def set_host(host):
    HOST = host

def main():
    #set_speed(25)
    while True:
        # index = separate_floor_from_obstacles()
        CheckGround()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        tcpCliSock.close()