#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules

import stream_client as sc
import color_gradient_selector as cgs
import white_lines as wl
import os
import time
import pid

HOST = '10.1.10.106'    # Server(Raspberry Pi) IP address
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


def main():
	wl.set_host(HOST)
	pid_obj = pid.PID(KP, KD, KI)

	turn_home()
	set_speed(50)
	forward()
	prev_dt = time.time()

	while True:
		# Din modulul lui Vasile -> getState()
		# returneaza distanta pana in marginea stanga si pana in marginea dreapta
		# + lista de obiecte
		left, right = wl.get_white_line_index()
		print "Left: ", left, " Right:", right

		error = left + right
		# print error
		if (error <= PERMITTED_ERROR):
			turn_home()
			set_speed(50)
			continue

		dt = time.time() - prev_dt
		prev_dt = time.time()
		increase = pid_obj.calculate(dt, 0, error)
		# Apel pid pentru distanta stanga dreapta => decizie
		print increase
		if abs(increase) < THRESHOLD:
			if increase > 0:
				turn_slight_left()
			else:
				turn_slight_right()
		else:
			if increase > 0:
				set_speed(35)
				turn_left()
			else:
				set_speed(35)
				turn_right()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		tcpCliSock.close()
