import picar_4wd as fc
import time
import sys
import numpy as np


def move_turn(power, diff):
	fc.left_front.set_power(power + diff)
	fc.left_rear.set_power(power + diff)
	fc.right_front.set_power(power - diff)
	fc.right_rear.set_power(power - diff)

try:
		
	#speed: 1 to 5: {2, 5, 10, 25, 50}
	#		-5 to -1: {-50, -25, -10, -5, -2}
	#speed = 0, then we turn in place
	#angle: 1 to 5: {} #turned towards right
	#		-5 to -1: {} #turned towards left
	#angle = 0, we go straight
	
	speed = 0
	angle = 0
	
	try:
		speed = int(sys.argv[2])
		angle = int(sys.argv[4])
	except:
		print("Incorrect values for speed and angle")
	
	speeds = np.concatenate([[0],np.linspace(30, 100, 5)])
	angles = np.concatenate([[0],np.linspace(7, 15, 5)])
	
	sign = 1 if speed == 0 else np.sign(speed)
	actual_speed = speeds[np.abs(speed)] * sign
	diff = angles[angle] * (np.abs(speed) + 1) * sign * np.sign(angle)
	
	move_turn(actual_speed, diff)	
	
		
finally:
    pass
