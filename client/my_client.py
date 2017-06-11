#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules
import time

HOST = '10.1.10.108'    # Server(Raspberry Pi) IP address
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
	while True:
		# Din modulul lui Vasile -> getState()
		# returneaza distanta pana in marginea stanga si pana in marginea dreapta
		# + lista de obiecte 

		# Apel pid pentru distanta stanga dreapta => decizie
		set_speed(40)
		forward()
		time.sleep(10)
		# turn_slight_right()
		time.sleep(1)
		set_speed(100)
		time.sleep(1)

		turn_home()
		backward()
		time.sleep(2)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		tcpCliSock.close()