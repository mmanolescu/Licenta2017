#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules
import time

import stream_client as sc
import color_gradient_selector as cgs
import cv2
import os
import numpy as np

HOST = '10.1.0.1'    # Server(Raspberry Pi) IP address
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
	gray = cgs.select_rgb_white_yellow(imgFile)
	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
	#edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

	cv2.imshow('image', gray)
	cv2.waitKey(1)


	H, L = gray.shape
	indexLeft = None
	maxVal = None

	for i in range(11, L/2 - 11):
		s = 0
		for j in range(i - 5, i + 5):
			s = s + gray[100][j]
		if indexLeft == None:
			indexLeft = i
		elif s > maxVal:
			indexLeft = i
			maxVal = s

	indexRight = None
	maxVal = None

	for i in range(L/2, L - 11):
		s = 0
		for j in range(i - 5, i + 5):
			s = s + gray[100][j]
		if indexRight == None:
			indexRight = i
		elif s > maxVal:
			indexRight = i
			maxVal = s

	H, L = gray.shape
	return indexLeft, indexRight


def main():
	#set_speed(25)
	last = None
	while True:
		indexLeft, indexRight = get_white_line_index()
		print indexLeft, indexRight


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		tcpCliSock.close()