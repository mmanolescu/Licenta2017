#!/usr/bin/env python
import RPi.GPIO as GPIO
import car_dir
import motor
from socket import *
import time          # Import necessary modules
import sys, os, traceback
import select
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

HOME = 'HOME'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
SLIGHT_LEFT = 'SLEFT'
SLIGHT_LEFT_ANGLE = 80
SLIGHT_RIGHT = 'SRIGHT'
SLIGHT_RIGHT_ANGLE = 175
FORWARD = 'FORWARD'
BACKWARD = 'BACKWARD'
SPEED = 'SPEED='

EMERGENCY_TIMEOUT = 0.5
EMERGENCY_STOP = False
# Streamer thread class to send images via HTTP
class MJPGStreamerThread(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		print 'MJPGStreamer Thread started.\n'
		dirname = "../mjpg-streamer/mjpg-streamer/"
		os.chdir(dirname)
		command = "./start.sh > /dev/null 2>&1"
		os.system(command)

class EmergencyModule(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		print 'Emergency Module started.\n'
		# Call Obstacle avoidance, if bad => EMERGENCY_STOP
		while True:
			pass

def setup():
	# Setup and calibrate direction and motor
	car_dir.setup(busnum=busnum)
	motor.setup(busnum=busnum)
	car_dir.home()

	# Starting streamer thread for image processing
	mjpg_st_th = MJPGStreamerThread()
	mjpg_st_th.start()

	em_th = EmergencyModule()
	em_th.start()

def loop():
	while True:
		print 'Waiting for connection...'
		# accept() is blocking until a new connection has been made
		tcpCliSock, addr = tcpSerSock.accept()
		print '...connected from :', addr

		while True:
			if (EMERGENCY_STOP == True)
				emergency_stop()

			ready = select.select(socket, [], [], EMERGENCY_TIMEOUT)
			if ready[0]:
				data = ''
				data = tcpCliSock.recv(BUFSIZ)    # Receive data sent from the client.
			else:
				emergency_stop()
				break
			if data == HOME:
				turn_home()
			elif data == LEFT:
				turn_left()
			elif data == RIGHT:
				turn_right()
			elif data == SLIGHT_LEFT:
				turn_angle(SLIGHT_LEFT_ANGLE)
			elif data == SLIGHT_RIGHT:
				turn_angle(SLIGHT_RIGHT_ANGLE)
			elif data == FORWARD:
				forward()
			elif data == BACKWARD:
				backward()
			elif data.startswith(SPEED) == True:
				spd = data.split('=', 1)[1]
				try:
					print spd
					speed = int(spd)
					print speed
					set_speed(speed)
				except Exception:
					print 'Set speed transmitted incorrect: ', spd
					print(traceback.format_exc())
			else:
				print 'Unrecognized command: ', data

			# Send ACK that command was processed and client cand send new command
			tcpCliSock.send('ACK')

		# In case connection is lost we should stop the car
		emergency_stop()

def turn_right():
	car_dir.turn_right()

def turn_left():
	car_dir.turn_left()

def turn_home():
	car_dir.home()

def turn_angle(angle):
	car_dir.turnS(angle)

def forward():
	motor.forward()

def backward():
	motor.backward()

def set_speed(spd):
	motor.setSpeed(spd)

def emergency_stop():
	turn_home()
	set_speed(0)

def main():
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		set_speed(0)
		tcpSerSock.close()

if __name__ == "__main__":
	main()

# For testing and debug 
def test():
	# motor.setSpeed(100)
	# motor.forward()

	time.sleep(1)
	
	turn_angle(180)
	# turn_right()

	time.sleep(1)

	turn_home()

	time.sleep(1)
	# motor.ctrl(0)
	# motor.setSpeed(0)	

def back():
	# motor.setSpeed(100)
	# motor.backward()

	time.sleep(2.8)

	# motor.setSpeed(0)
