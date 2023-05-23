# Gesture Controlled Robot

## Dependencies

mediapipe==0.9.3.0 \
opencv-python==4.7.0.72 \
paramiko \
numpy

## Execution
1. Create a hotspot with name lmlrobotics and password Staratio10!
2. Check picar-4wd ip address using the phone that is generating the hotspot.
3. Connect your pc to the hotspot
4. Clone this github repository (hand-gesture) on the robot's computer inside of the directory picar-4wd/
5. Run the command:
 `python3 run.py --hostname ip_address`
replacing ip_address by the robot's ip address.
1. If you wish to try the gesture detection without connecting to a robot you can use:
 `python3 run.py --no_robot`


