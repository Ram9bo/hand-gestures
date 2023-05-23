import picar_4wd as fc
import sys
import numpy as np


def move_turn(power, diff):
	fc.left_front.set_power(power + diff)
	fc.left_rear.set_power(power + diff)
	fc.right_front.set_power(power - diff)
	fc.right_rear.set_power(power - diff)

try:

	speed = 0
	angle = 0
	
	try:
		# Read angle and speed from command
		speed = int(sys.argv[2])
		angle = int(sys.argv[4])
	except:
		print("Incorrect values for speed and angle")
	
	# Speed levels to power
	powers = np.concatenate([[0],np.linspace(30, 100, 5)])

	# Angle level to power difference from one wheel to other
	diffs = np.concatenate([[0],np.linspace(7, 15, 5)])
	
	speed_sign = 1 if speed == 0 else np.sign(speed)
	actual_speed = powers[np.abs(speed)] * speed_sign
	# Difference proportional to speed
	diff = diffs[np.abs(angle)] * (np.abs(speed) + 1) * speed_sign * np.sign(angle)
	
	move_turn(actual_speed, diff)	
	
		
finally:
    pass
