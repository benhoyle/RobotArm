# ROBOT ARM CONTROL PROGRAM
# import the USB and Time libraries into Python
import usb.core, usb.util, time, thread
#import xml libraries
import elementtree.ElementTree as ET

def Initialise():
	# Allocate the name 'RoboArm' to the USB device
	RoboArm = usb.core.find(idVendor=0x1267, idProduct=0x0000)
	
	# Check if the arm is detected and warn if not
	if RoboArm is None:
		raise ValueError("Arm not found")
	#improve by making RoboArm an object with properties and movearm method
	return RoboArm

# Define a procedure to execute each movement
def MoveArm(RoboArm, Duration, ArmCmd):
	# Start the movement
	RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
	# Stop the movement after waiting specified duration
	time.sleep(Duration)
	ArmCmd=[0,0,0]
	RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
	
def input_thread(L):
   raw_input()
   L.append(None)
	
def MeasureLoop(RoboArm, T, ArmCmd):
	unitcount = 0
	i = raw_input("Press return to start then stop arm")
	
	L = []
	thread.start_new_thread(input_thread, (L,))
	while 1:
		if L:
			break
		#test with next line commented?
		MoveArm(RoboArm, T, ArmCmd)
		#time.sleep(T) #testline
		unitcount = unitcount +1
	print("Key pressed:movement halted")
	print("Movement units: ", unitcount)
	return unitcount

def MeasureDim(RoboArm, T, ArmCmds):
	print("Running movement in first direction")
	#Run loop in one direction
	uc1 = MeasureLoop(RoboArm, T, ArmCmds[0])
	
	print("Running movement in second direction")
	#Run loop in other direction
	uc2 = MeasureLoop(RoboArm, T, ArmCmds[1])
	
	dim_range = uc1+uc2
	
	#Centre arm in dimension
	centreunits = dim_range/2
	print centreunits
	MoveArm(RoboArm, centreunits*T, ArmCmds[0])
	
	return dim_range, centreunits

def CheckGrip():
	grip_state = raw_input("Is grip open? Type Y for Yes or N for No")
	if grip_state.lower() == "y":
		grip_state = True
	else:
		grip_state = False
	return grip_state

def StoreValues(ranges_values, positions_values, grip_state):
	configfile = ET.Element("configfile")
	ranges = ET.SubElement(configfile, "ranges")
	i = 0
	for range_value in ranges_values:
		element = ET.SubElement(ranges, ( "range_"+str(i)))
		element.text = str(range_value)
		i=i+1
		#0 is base; 1 is shoulder; 2 is elbow; 3 is wrist
		
	positions = ET.SubElement(configfile, "positions")
	i = 0
	for position_value in positions_values:
		element = ET.SubElement(positions, ( "position_"+str(i)))
		element.text = str(position_value)
		i = i +1
		#0 is base; 1 is shoulder; 2 is elbow; 3 is wrist
		
	gripstate = ET.SubElement(configfile, "gripstate")
	gripstate.text = str(grip_state)
	xml_fn = "config.xml"
	tree = ET.ElementTree(configfile)
	tree.write(xml_fn)

# Create a variable for duration
T=0.5
RoboArm = Initialise()
#0 is base; 1 is shoulder; 2 is elbow; 3 is wrist
ranges_values = []
positions_values = []
commands = [([0,1,0], [0,2,0]), ([64,0,0], [128,0,0]), ([16,0,0], [32,0,0]), ([4,0,0], [8,0,0])]
for i in range(0,4):
	rv, pv = MeasureDim(RoboArm, T, commands[i])
	ranges_values.append(rv)
	positions_values.append(pv)
grip_state = CheckGrip()
print ranges_values, positions_values, grip_state
StoreValues(ranges_values, positions_values, grip_state)

#Ask user whether grip is open or closed?
#Write current position to file?

#MoveArm(1,[0,1,0]) #Rotate base anticlockwise
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


