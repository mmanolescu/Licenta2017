#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules
import time

import stream_client as sc
import color_gradient_selector as cgs
import cv2
import os
import numpy as np

HOST = '10.1.10.106'    # Server(Raspberry Pi) IP address
PORT = 21567
ADDR = (HOST, PORT)

TMP_FILE = 'tmp.jpg'

def get_white_line_index():
	img = sc.get_next_jpeg()

	#os.remove(TMP_FILE)
	f = open(TMP_FILE, 'wb')
	f.write(img)
	f.close()

	imgFile = cv2.imread(TMP_FILE, cv2.CV_LOAD_IMAGE_COLOR)
	half_img = cv2.resize(imgFile, (0,0), fx=0.5, fy=0.5)
	gray = cgs.select_rgb_white_yellow(half_img)
	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

	height, width = gray.shape

	l = []
	for x in range(height/2, height, 20):
		maxSum = 0
		index = 0
		flag = True
		s = 0
		for i in range(11, width - 12):
			if flag == True:
				for j in range(i - 5, i + 5):
					s = s + gray[x][j]
				flag = False
			else:
				s = s - gray[x][i - 5 - 1] + gray[x][i + 5 - 1]

			if s > maxSum:
				maxSum = s
				index = i
		l.append(index)



	cv2.imshow('image', gray)
	cv2.waitKey(1)

	return np.sum(l) / len(l)

from time import gmtime, strftime

def main():
	#set_speed(25)
	last = None
	start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	while True:
		index = get_white_line_index()
	end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

	print start_time
	print end_time


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		tcpCliSock.close()