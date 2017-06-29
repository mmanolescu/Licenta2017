#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules
import time

import stream_client as sc
import color_gradient_selector as cgs
import cv2
import os
import numpy as np

HOST = '192.168.100.17'    # Server(Raspberry Pi) IP address
PORT = 21567
ADDR = (HOST, PORT)
CENTER_INDEX = 320

TMP_FILE = 'tmp.jpg'

last_good_index = 0

def get_white_line_index():
	global last_good_index
	img = sc.get_next_jpeg()

	#os.remove(TMP_FILE)
	f = open(TMP_FILE, 'wb')
	f.write(img)
	f.close()

	imgFile = cv2.imread(TMP_FILE, cv2.CV_LOAD_IMAGE_COLOR)
	half_img = cv2.resize(imgFile, (0,0), fx=0.5, fy=0.5)
	gray = cgs.select_rgb_white_yellow(half_img)
	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

	#gray = cv2.blur(gray,(5,5))
	#gray = cv2.blur(gray,(5,5))

	height, width = gray.shape

	l = []
	ys = []
	for x in range(height/3, height, 20):
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

		print maxSum / 10, 

		
		if maxSum / 10 < 90:
			break

		l.append(index)
		ys.append(x)

	print "-------"

	if len(l) > 0:
		index = (int) (np.sum(l) / len(l))
	else:
		index = last_good_index

	i = 0
	for i in range(len(l)):
			tmp = l[i]
			cv2.circle(half_img, (tmp, ys[i]), 15, (255, 0, 0), thickness=10)
			i = i + 1

	cv2.line(half_img, (index, height - 1), (index, height/2), (0, 0, 255), 6)

	cv2.imshow('image', half_img)
	cv2.waitKey(1)

	if index == 0:
		return last_good_index
	else:
		last_good_index = index
		return last_good_index



def set_host(host):
	HOST = host

def main():
	#set_speed(25)
	while True:
		index = get_white_line_index()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		tcpCliSock.close()
