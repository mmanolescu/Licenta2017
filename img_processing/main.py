
import stream_client as sc
import color_gradient_selector as cgs
import cv2
import os
import numpy as np

TMP_FILE = 'tmp.jpg'
OUT_FILE = 'out-1.jpg'

def get_road_lines_coordinates(img):
	return (-1, 1)

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

		imgFile = cv2.imread(TMP_FILE, cv2.CV_LOAD_IMAGE_COLOR)
		half_img = cv2.resize(imgFile, (0,0), fx=0.5, fy=0.5)
		gray = cgs.select_rgb_white_yellow(imgFile)
		#gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
		#edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

		cv2.imshow('image', gray)
		cv2.waitKey(0)

		# Get left and right road_lines coordinates
		# left margin of image is -1
		# right margin of image is
		left_line, right_line = get_road_lines_coordinates(gray)


