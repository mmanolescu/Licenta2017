#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules
import time

import stream_client as sc
import color_gradient_selector as cgs
import cv2
import os
import numpy as np

CENTER_INDEX = 320

TMP_FILE = 'tmp.jpg'

def get_obstacles():
	img = sc.get_next_jpeg()

	#os.remove(TMP_FILE)
	f = open(TMP_FILE, 'wb')
	f.write(img)
	f.close()

	imgFile = cv2.imread(TMP_FILE, cv2.CV_LOAD_IMAGE_COLOR)
	half_img = cv2.resize(imgFile, (0,0), fx=0.5, fy=0.5)
	gray = cv2.cvtColor(half_img, cv2.COLOR_BGR2GRAY)

	ret, thresh = cv2.threshold(gray, 127, 255, 0)
	im2, contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	print len(contours)

	cv2.drawContours(half_img, contours, -1, (0,255,0), 3)

	cv2.imshow('image', half_img)
	cv2.waitKey(1)

def main():
	#set_speed(25)
	while True:
		get_obstacles()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		tcpCliSock.close()