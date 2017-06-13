#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules
import time
import pid

import stream_client as sc
import color_gradient_selector as cgs
import cv2
import os
import numpy as np

HOST = '10.1.0.1'    # Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024             # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
tcpCliSock.connect(ADDR)                    # Connect with the server

HOME = 'HOME'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
SLIGHT_LEFT = 'SLEFT'
SLIGHT_RIGHT = 'SRIGHT'
FORWARD = 'FORWARD'
BACKWARD = 'BACKWARD'
SPEED = 'SPEED='

# GainzZz for pid algorithm
KP = 0.1
KD = 0.01
KI = 0.5
THRESHOLD = 5
PERMITTED_ERROR = 10

def send_command(cmd):
	tcpCliSock.sendall(cmd)
	ack_data = tcpCliSock.recv(BUFSIZ)

def turn_home():
	send_command(HOME)

def turn_left():
	send_command(LEFT)

def turn_slight_left():
	send_command(SLIGHT_LEFT)

def turn_right():
	send_command(RIGHT)

def turn_slight_right():
	send_command(SLIGHT_RIGHT)

def forward():
	send_command(FORWARD)

def backward():
	send_command(BACKWARD)

def set_speed(spd):
	if spd > 100:
		spd = 100
	elif spd < 0:
		spd = 0
	send_command(SPEED + str(spd))



TMP_FILE = 'tmp.jpg'

def in_borders(index):
	if index < 300:
		return -1

	if index > 400:
		return 1

	return 0


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
	print L
	return indexLeft, indexRight


def main():
	pid_obj = PID(KP, KD, KI)

	turn_home()
	set_speed(50)
	forward()
	prev_dt = time.time()

	while True:
		# Din modulul lui Vasile -> getState()
		# returneaza distanta pana in marginea stanga si pana in marginea dreapta
		# + lista de obiecte
		left = 0
		right = 0

		error = left + right
		print error
		if (error <= PERMITTED_ERROR)
			turn_home()
			set_speed(100)
			continue

		dt = time.time() - prev_dt
		prev_dt = time.time()
		increase = pid_obj.calculate(dt, 0, error)
		# Apel pid pentru distanta stanga dreapta => decizie

		if abs(increase) < THRESHOLD:
			if increase > 0:
				turn_slight_left()
			else:
				turn_slight_right()
		else:
			if increase > 0:
				set_speed(50)
				turn_left()
			else:
				set_speed(50)
				turn_right()


if __name__ == '__main__':
	try:
		init()
		main()
	except KeyboardInterrupt:
		tcpCliSock.close()