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

HOST = '10.1.10.105'    # Server(Raspberry Pi) IP address
PORT = 21567
ADDR = (HOST, PORT)
CENTER_INDEX = 320

TMP_FILE = 'tmp3.jpg'


def get_next_object_index():

    StepSize = 6
    EdgeArray = []

    orig_img = sc.get_next_jpeg()

    os.remove(TMP_FILE)
    f = open(TMP_FILE, 'wb')
    f.write(orig_img)
    f.close()

    imgFile = cv2.imread(TMP_FILE, cv2.CV_LOAD_IMAGE_COLOR)
    img = cv2.resize(imgFile, (0,0), fx=0.5, fy=0.5)

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #convert img to grayscale and store result in imgGray
    imgGray = cv2.bilateralFilter(imgGray,9,30,30) #blur the image slightly to remove noise
    imgEdge = cv2.Canny(imgGray, 20, 200)             #edge detection

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



    left1, right1, maxValue = getNextObstaclePosition(EdgeArray, img)
    print left1, right1, maxValue

    cv2.line(img, (left1, maxValue), (right1, maxValue), (0,0,255), 10)
    cv2.imshow("camera", img)
    cv2.waitKey(1)

    return left1, right1, maxValue

    left1, right1, maxValue = getNextObstaclePosition(EdgeArray, img)
    print left1, right1, maxValue

    cv2.line(img, (left1, maxValue), (right1, maxValue), (0,0,255), 10)


    left1, right1, maxValue = getNextObstaclePosition(EdgeArray, img)
    print left1, right1, maxValue

    cv2.line(img, (left1, maxValue), (right1, maxValue), (0,0,255), 10)


    # print EdgeArray

    # cv2.imshow("camera", img)
    # cv2.waitKey(0)


def getNextObstaclePosition(vec, img):
    '''
    vec is a vector of (j, i) elements where i is hight at j position
    '''

    minValue, minPos = 1000, 0
    maxValue, maxPos = 0, 0

    for x in range( len(vec) - 1 ):
        j, i = vec[x]
        if i < minValue:
            minValue = i
            minPos = x
        if i > maxValue:
            maxValue = i
            maxPos = x

    '''
    -----       -------
         -     -
          -   -
           ---
           minPos
    '''

    minDim = 2
    print maxValue, maxPos

    right = maxPos + 1 + minDim
    while right < len(vec) - 1 and vec[right][1] == vec[right - 1][1]:
        right = right + 1
    while right < len(vec) - 1 and vec[right][1] > vec[right - 1][1]:
        right = right + 1

    left = maxPos - minDim
    while left > 0 and vec[left][1] == vec[left + 1][1]:
        left = left - 1
    while left > 0 and vec[left][1] >= vec[left + 1][1]:
        left = left - 1

    if left < 0:
        left = 0
    if right >= len(vec):
        right = len(vec) - 1

    for x in range(left, right):
        j, i = vec[x]
        vec[x] = j, minValue

    return left * 6, right * 6, maxValue





def set_host(host):
    HOST = host

def main():
    #set_speed(25)
    while True:
        # index = separate_floor_from_obstacles()
        get_next_object_index()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        tcpCliSock.close()
