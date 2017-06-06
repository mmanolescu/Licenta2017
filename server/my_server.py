#!/usr/bin/env python
import RPi.GPIO as GPIO
import car_dir
import motor
from socket import *
import time          # Import necessary modules
import sys, os
from threading import Thread


HOST = ''           # The variable of HOST is null, so the function bind( ) can be bound to all valid addresses.
PORT = 21567
BUFSIZ = 1024       # Size of the buffer
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)    # Create a socket.
tcpSerSock.bind(ADDR)    # Bind the IP address and port number of the server. 
tcpSerSock.listen(5)     # The parameter of listen() defines the number of connections permitted at one time. Once the 
                         # connections are full, others will be rejected. 

busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0

class MJPGStreamerThread(Thread):
	def __init__(self):
		pass

	def run(self):



def setup():
	car_dir.setup(busnum=busnum)
	motor.setup(busnum=busnum)
	car_dir.home()

def turn_right():
	car_dir.turn_right()

def turn_left():
	car_dir.turn_left()

def turn_home():
	car_dir.home()

def turn_angle(angle):
	car_dir.turn(angle)

def test():
	motor.setSpeed(100)
	motor.forward()

	time.sleep(1)
	
	turn_angle(180)
	# turn_right()

	time.sleep(1)

	turn_home()

	time.sleep(1)
	motor.ctrl(0)
	motor.setSpeed(0)	

def back():
	motor.setSpeed(100)
	motor.backward()

	time.sleep(2.8)

	motor.setSpeed(0)

if __name__ == "__main__":
	try:
		setup()
		test()
		back()
	except KeyboardInterrupt:
		tcpSerSock.close()
