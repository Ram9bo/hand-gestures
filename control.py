import picar_4wd as fc
import time
import sys
import numpy as np


def move_turn(power, diff):
	print("pow-diff", power-diff)
	print("pow+diff", power+diff)
	
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
		print("Speed: ", speed)
		print("Angle: ", angle)
	except:
		print("Incorrect values for speed and angle")
	
	positive_speeds = np.linspace(30, 100, 5)
	negative_speeds = np.linspace(-100, -30, 5)
	
	positive_angles = np.linspace(7, 15, 5)
	negative_angles = np.linspace(-15, -7, 5)
	

	if speed < 0:
		actual_speed = negative_speeds[5+speed]
	elif speed > 0:
		actual_speed = positive_speeds[speed-1]
	else:
		actual_speed = 0
		
	print("Actual speed: ", actual_speed)
	sign = 1 if speed == 0 else np.sign(speed)
	
	if angle < 0:
		diff = negative_angles[5+angle] * (np.abs(speed) + 1) * sign
	elif angle > 0:
		diff = positive_angles[angle-1]  * (np.abs(speed) + 1) * sign
	else:
		diff = 0	
	
	print("Diff: ", diff)
	
	
	move_turn(actual_speed, diff)	
	
		
finally:
    pass
