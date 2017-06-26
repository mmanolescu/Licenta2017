#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules
import time

import stream_client as sc
import color_gradient_selector as cgs
import cv2
import os
import numpy as np

HOST = '10.1.10.101'    # Server(Raspberry Pi) IP address
PORT = 21567
ADDR = (HOST, PORT)
CENTER_INDEX = 320

TMP_FILE = 'tmp.jpg'
TMP_FILE1 = '2-lines-detected.jpg'

last_good_index = 0

def filter_region(image, vertices):
	"""
	Create the mask using the vertices and apply it to the input image
	"""
	mask = np.zeros_like(image)
	if len(mask.shape)==2:
		cv2.fillPoly(mask, vertices, 255)
	else:
		cv2.fillPoly(mask, vertices, (255,)*mask.shape[2]) # in case, the input image has a channel dimension
	return cv2.bitwise_and(image, mask)

def select_region(image):
	"""
	It keeps the region surrounded by the `vertices` (i.e. polygon).  Other area is set to 0 (black).
	"""

	rows, cols = image.shape[0:2]
	# first, define the polygon by vertices
	rows, cols = image.shape[:2]
	bottom_left  = [0, rows*0.9]
	top_left     = [cols*0.4, rows*0.5]
	bottom_right = [cols, rows*0.9]
	top_right    = [cols*0.6, rows*0.5]
	# the vertices are an array of polygons (i.e array of arrays) and the data type must be integer
	vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
	return filter_region(image, vertices)

def get_lines_points(img):

	rows, cols = img.shape
	print rows, cols

	# search left line at altitude (rows - 30) pixels
	i = rows - 30
	left1 = 0

	for j in range(0, cols - 5):
		s = img[i][j] + img[i][j + 1] + img[i][j + 2] + img[i][j + 3]
		if s > 30 * 4:
			left1 = j
			break

	p1 = (left1, i)

	# search left line at altitude (rows - 60) pixels
	i = rows - 80
	left2 = 0

	for j in range(0, cols - 5):
		s = img[i][j] + img[i][j + 1] + img[i][j + 2] + img[i][j + 3]
		if s > 30 * 4:
			left2 = j
			break

	p2 = (left2, i)

	# search right line at altitude (rows - 30) pixels
	i = rows - 30
	right1 = 0

	for j in range(cols - 1, 5, -1):
		s = img[i][j] + img[i][j - 1] + img[i][j - 2] + img[i][j - 3]
		if s > 30 * 4:
			right1 = j
			break

	p3 = (right1, i)

	# search right line at altitude (rows - 60) pixels
	i = rows - 80
	right2 = 0

	for j in range(cols - 1, 5, -1):
		s = img[i][j] + img[i][j - 1] + img[i][j - 2] + img[i][j - 3]
		if s > 30 * 4:
			right2 = j
			break

	p4 = (right2, i)


	return p1, p2, p3, p4



def get_white_line_index():
	global last_good_index
	#img = sc.get_next_shoot()

	#os.remove(TMP_FILE)
	#f = open(TMP_FILE, 'wb')
	#f.write(img)
	#f.close()

	imgFile = cv2.imread(TMP_FILE, cv2.CV_LOAD_IMAGE_COLOR)
	half_img = cv2.resize(imgFile, (0,0), fx=0.5, fy=0.5)
	half_img = select_region(half_img)
	gray = cgs.select_rgb_white_yellow(half_img)
	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

	gray = cv2.imread('tmp1.jpg')
	gray = select_region(gray)
	half_img = gray
	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

	height, width = gray.shape
	print "---", height, width

	p1, p2, p3, p4 = get_lines_points(gray)
	print p1, p2, p3, p4

	cv2.line(half_img, p1, p2, (255, 0, 0), 3)
	cv2.line(half_img, p3, p4, (255, 0, 0), 3)

	#M = perspTransform(gray)
	#sz = np.array([width - 1, height - 1], np.float32)
	#warped = cv2.warpPerspective(gray, M, ((width - 1), height - 1))

	edges = cv2.Canny(gray, 100, 200)
	minLineLength = 10
	maxLineGap = 10
	lines = cv2.HoughLinesP(edges, 1, np.pi/180, 80, 50, 20)
	for x1,y1,x2,y2 in lines[0]:
	    cv2.line(gray,(x1,y1),(x2,y2),(0,255,0),2)

	cv2.imshow('image', half_img)
	cv2.waitKey(1)

	cv2.imwrite('edged.jpg', edges)
	cv2.imwrite('lines-hough.jpg', half_img)

def perspTransform(image):
	rows, cols = image.shape[0:2]

	top_left     = [cols*0.4, rows*0.5]
	top_right    = [cols*0.6, rows*0.5]
	bottom_right = [cols, rows*0.9]
	bottom_left  = [0, rows*0.9]

	A = np.array([top_left, top_right, bottom_right, bottom_left], np.float32)
	B = np.array([[0, 0], [cols - 1, 0], [cols - 1, rows - 1], [0, rows - 1]], np.float32)

	ptransf = cv2.getPerspectiveTransform(A, B)

	return ptransf

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