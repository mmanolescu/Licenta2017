
#import stream_client as sc
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
		#img = sc.get_next_jpeg()

		#os.remove(TMP_FILE)
		#f = open(TMP_FILE, 'wb')
		#f.write(img)
		#f.close()

		imgFile = cv2.imread(TMP_FILE, cv2.CV_LOAD_IMAGE_COLOR)
		half_img = cv2.resize(imgFile, (0,0), fx=0.5, fy=0.5)
		gray = cgs.select_rgb_white_yellow(half_img)
		gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

		lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
		for rho,theta in lines[0]:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))

			cv2.line(gray, (x1,y1), (x2,y2), (0, 0, 255), 2)


		cv2.imshow('image', gray)
		cv2.waitKey(0)

		# Get left and right road_lines coordinates
		# left margin of image is -1
		# right margin of image is
		left_line, right_line = get_road_lines_coordinates(gray)


