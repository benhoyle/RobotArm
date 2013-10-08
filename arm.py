# ROBOT ARM CONTROL PROGRAM
# import the USB and Time libraries into Python
import usb.core, usb.util, time

# Allocate the name 'RoboArm' to the USB device
RoboArm = usb.core.find(idVendor=0x1267, idProduct=0x0000)

# Check if the arm is detected and warn if not
if RoboArm is None:
	raise ValueError("Arm not found")

# Create a variable for duration
Duration=1

# Define a procedure to execute each movement
def MoveArm(Duration, ArmCmd):
	# Start the movement
	RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
	# Stop the movement after waiting specified duration
	time.sleep(Duration)
	ArmCmd=[0,0,0]
	RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)

MoveArm(1,[0,1,0]) #Rotate base anticlockwise
#MoveArm(2,[0,2,0]) #Rotate base clockwise
#MoveArm(1,[64,0,0]) #Shoulder Up
#MoveArm(1,[128,0,0]) #Shoulder Down
#MoveArm(1,[16,0,0]) #Elbow Up
#MoveArm(1,[32,0,0]) #Elbow Down
#MoveArm(1,[4,0,0]) #Wrist Up
#MoveArm(1,[8,0,0]) #Wrist Down
#MoveArm(0.5,[2,0,0]) #Grip Open
#MoveArm(0.5,[1,0,0]) #Grip Close
#MoveArm(1,[0,0,1]) #Light On
#MoveArm(1,[0,0,0]) #Light Off



