#!/usr/bin/env python
import RPi.GPIO as GPIO
import car_dir
import motor
from socket import *
from time import ctime          # Import necessary modules

HOST = ''           # The variable of HOST is null, so the function bind( ) can be bound to all valid addresses.
PORT = 21567
BUFSIZ = 1024       # Size of the buffer
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)    # Create a socket.
tcpSerSock.bind(ADDR)    # Bind the IP address and port number of the server. 
tcpSerSock.listen(5)     # The parameter of listen() defines the number of connections permitted at one time. Once the 
                         # connections are full, others will be rejected. 

busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0

def setup():
	global offset_x, offset_y, offset, forward0, forward1
	offset_x = 0
	offset_y = 0
	offset = 0
	forward0 = 'True'
	forward1 = 'False'
	try:
		for line in open('config'):
			if line[0:8] == 'offset_x':
				offset_x = int(line[11:-1])
				print 'offset_x =', offset_x
			if line[0:8] == 'offset_y':
				offset_y = int(line[11:-1])
				print 'offset_y =', offset_y
			if line[0:8] == 'offset =':
				offset = int(line[9:-1])
				print 'offset =', offset
			if line[0:8] == "forward0":
				forward0 = line[11:-1]
				print 'turning0 =', forward0
			if line[0:8] == "forward1":
				forward1 = line[11:-1]
				print 'turning1 =', forward1
	except:
		print 'no config file, set config to original'
	car_dir.setup(busnum=busnum)
	motor.setup(busnum=busnum)
	car_dir.calibrate(offset)

def test():
	motor.setSpeed(50)
	motor.forward()
	time.sleep(50)
	motor.setSpeed(0)


if __name__ == "__main__":
	try:
		setup()
		test()
	except KeyboardInterrupt:
		tcpSerSock.close()
