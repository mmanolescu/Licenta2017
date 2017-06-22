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

HOST = '10.1.10.101'    # Server(Raspberry Pi) IP address
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
	D = width / 30

	#gray = h

	obstaclePos = []
	for index in range(D, width - D, D):
		obstaclePos.append(0)
		#cv2.rectangle(gray, (index, height - D), (index + D, height - 1), (255, 0, 0), 3)
		floor = gray[(height - D):height, index:(index + D) ]

		mean_value = floor.mean()
		print 'mean value: ', mean_value

		for k in range(2, 7):
			#cv2.rectangle(gray, (index, height - k*D), (index + D, height - - (k - 1) * D), (255, 0, 0), 3)
			rect = gray[(height - k*D):(height - (k - 1) * D), index:(index + D) ]

			m = rect.mean()
			print m, m - mean_value

			#cv2.rectangle(gray, (index, height - k * D), (index + D, height - k * D - D), (255, 0, 0), 3)
			if abs(m - mean_value) > 10:
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
	cv2.imshow('image', half_img)
	cv2.waitKey(1)

	return None



def set_host(host):
	HOST = host

def main():
	#set_speed(25)
	while True:
		index = separate_floor_from_obstacles()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		tcpCliSock.close()