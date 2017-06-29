#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules

import stream_client as sc
import color_gradient_selector as cgs
import white_lines as wl
import floor_obstacles as fl
import os
import numpy as np
import white_lines
import time
import pid

HOST = '192.168.100.17'    # Server(Raspberry Pi) IP address
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
KP = 0.3
KD = 0.01
KI = 0.005

THRESHOLD = 20

PERMITTED_ERROR = 30
NORMAL_SPEED = 70
TURN_SPEED = 50
SLIGHT_TURN_SPEED = 60
MIDDLE_OF_ROAD = 160

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

# def test():
# 	last_move = None
# 	while True:
# 		index = white_lines.get_white_line_index()
# 		print index
# 		mid = 160

# 		dif = mid - index

# 		if abs(dif) < 20:
# 			turn_home()
# 		elif dif > 0:
# 			last_move = 'l'
# 			turn_left()
# 		else:
# 			last_move = 'r'
# 			turn_right()

# 		forward()

def main():

	wl.set_host(HOST)
	pid_obj = pid.PID(KP, KD, KI)

	turn_home()
	set_speed(NORMAL_SPEED)
	forward()
	prev_dt = time.time()

	fps = time.time()
	while True:
		# Din modulul lui Vasile -> getState()
		# returneaza distanta pana in marginea stanga si pana in marginea dreapta
		# + lista de obiecte
		index = wl.get_white_line_index()
		print "Index: ", index

		error = MIDDLE_OF_ROAD - index
		# print error
		if (abs(error) <= PERMITTED_ERROR):
			turn_home()
			set_speed(NORMAL_SPEED)
			continue

		dt = time.time() - prev_dt
		prev_dt = time.time()
		increase = pid_obj.calculate(0.1, 0, error)
		print "Increase: ", increase, " Error: ", error
		# Apel pid pentru distanta stanga dreapta => decizie
		if abs(increase) < THRESHOLD:
			set_speed(SLIGHT_TURN_SPEED)
			if increase < 0:
				turn_slight_left()
			else:
				turn_slight_right()
		else:
			set_speed(TURN_SPEED)
			if increase < 0:
				turn_left()
			else:
				turn_right()


def obstacles():
	fl.set_host(HOST)

	turn_home()
	set_speed(70)
	forward()

	fps = time.time()
	while True:
		print time.time() - fps
		fps = time.time()
		left, right, distance = fl.get_next_object_index()

		if distance > 230:
			while distance > 100:
				turn_home()
				backward()
				left, right, distance = fl.get_next_object_index()
			forward()
		elif distance > 30:
			if (MIDDLE_OF_ROAD - left > right - MIDDLE_OF_ROAD):
				turn_right()
			else:
				turn_left()
		else:
			turn_home()


if __name__ == '__main__':
	try:
		main()
		#obstacles()
	except KeyboardInterrupt:
		tcpCliSock.close()
