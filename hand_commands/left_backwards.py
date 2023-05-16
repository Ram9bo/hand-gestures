import ZeroBorg3 as ZeroBorg
#import ZeroBorg
import time

# Setup the ZeroBorg
ZB = ZeroBorg.ZeroBorg()
ZB.Init()

if not ZB.foundChip:
    boards = ZeroBorg.ScanForZeroBorg()
    if len(boards) == 0:
        print('No ZeroBorg found, check you are attached :)')
    else:
        print('No ZeroBorg at address %02X, but we did find boards:' % (
            ZB.i2cAddress))
        for board in boards:
            print('    %02X (%d)' % (board, board))
        print(
            'If you need to change the IÂ²C address change the setup line so it is correct, e.g.')
        print('ZB.i2cAddress = 0x%02X' % (boards[0]))
    sys.exit()
# ZB.SetEpoIgnore(True)                 # Uncomment to disable EPO latch, needed if you do not have a switch / jumper
# Ensure the communications failsafe has been enabled!
failsafe = False
for i in range(5):
    ZB.SetCommsFailsafe(True)
    failsafe = ZB.GetCommsFailsafe()
    if failsafe:
        break
if not failsafe:
    print('Board %02X failed to report in failsafe mode!' % (ZB.i2cAddress))
    sys.exit()
ZB.ResetEpo()
ZB.SetLed(False)

# Power settings
voltageIn = 9                        # Total battery voltage to the ZeroBorg (change to 9V if using a non-rechargeable battery)
voltageOut = 6.0                        # Maximum motor voltage

# Setup the power limits
if voltageOut > voltageIn:
    maxPower = 1.0
else:
    maxPower = voltageOut / float(voltageIn)
    
speed = 0.8
angle = 90
timeSpin360   = 1.7   # Number of seconds needed to make a full left...
numSeconds = (angle / 360.0) * timeSpin360
try:

    # Set the motors to the new speeds
    ZB.SetMotor1(0.9) # Rear right
    ZB.SetMotor2(0.9) # Front right
    ZB.SetMotor3(0.6) # Front left
    ZB.SetMotor4(0.6) # Rear left

    time.sleep(4.8)
    print(numSeconds)

    ZB.MotorsOff()

except e:
    ZB.MotorsOff()
    

