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
    
driveRight = 0.9
driveLeft = 0.6
angle = 90
timeSpin360   = 1.7   # Number of seconds needed to make a full left...
numSeconds = 10 * timeSpin360
def PerformMove(driveLeft, driveRight, numSeconds):
    # Set the motors to the new speeds
    ZB.SetMotor1(driveRight) # Rear right
    ZB.SetMotor2(driveRight) # Front right
    ZB.SetMotor3(driveLeft) # Front left
    ZB.SetMotor4(driveLeft) # Rear left

    time.sleep(numSeconds)
    print(numSeconds)

    ZB.MotorsOff()
    
PerformMove(driveLeft, driveRight, numSeconds)


    

