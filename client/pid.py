class PID():
	# dt - used to measure time between calculations
	# kp - proportional gain
	# kd - derivative gain
	# ki - derivative gain
	def __init__(self, kp, kd, ki):
		self.kp = kp
		self.kd = kd
		self.ki = ki
		self.integral = 0
		self.prev_error = 0

	# setpoint - the destination, will be 0
	# position - the current position
	def calculate(self, dt, setpoint, position):
		error = setpoint - position

		prop_out = self.kp * error

		self.integral += error * dt
		integral_out = self.ki * self.integral

		deriv = (error - self.prev_error) / dt
		deriv_out = self.kd * deriv

		output = prop_out + integral_out + deriv_out

		self.prev_error = error

		return output