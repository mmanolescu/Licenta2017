#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules

HOST = '192.168.0.147'    # Server(Raspberry Pi) IP address
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

def turn_home():
	tcpCliSock.send(HOME)

def turn_left():
	tcpCliSock.send(LEFT)

def turn_slight_left():
	tcpCliSock.send(SLIGHT_LEFT)

def turn_right():
	tcpCliSock.send(RIGHT)

def turn_slight_right():
	tcpCliSock.send(SLIGHT_RIGHT)

def forward():
	tcpCliSock.send(FORWARD)

def backward():
	tcpCliSock.send(BACKWARD)

def set_speed(spd):
	tcpCliSock.send(SPEED + spd)

def main():
	while True:
		# Din modulul lui Vasile -> getState()
		# returneaza distanta pana in marginea stanga si pana in marginea dreapta
		# + lista de obiecte 

		# Apel pid pentru distanta stanga dreapta => decizie



if __name__ == '__main__':
	main()