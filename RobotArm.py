# import the USB and Time libraries into Python
import usb.core, usb.util, time, thread
import elementtree.ElementTree as ET

class robot:
	def __init__(self):
		# Allocate the name 'RoboArm' to the USB device
		self.arm = usb.core.find(idVendor=0x1267, idProduct=0x0000)

		# Check if the arm is detected and warn if not
		if self.arm is None:
			raise ValueError("Arm not found")
		
		self.commands = [([0,1,0], [0,2,0]), ([64,0,0], [128,0,0]), ([16,0,0], [32,0,0]), ([4,0,0], [8,0,0])]
		self.duration = 0.5 #Period of time units
		
		#Load position and range values
		#Read XML file
		tree = ET.ElementTree(file='config.xml')
		
		#Access ranges tags
		for elem in tree.iter(tag='ranges'):
			self.ranges.append(elem.text)
			
		for elem in tree.iter(tag='positions'):
			self.positions.append(#tag value)
		
		#Access grip_state tag
		for elem in tree.iterfind('gripstate'):
			self.gripstate = elem.text
			
			
	def move(self, TimeUnits, AxisFlag, DirectionFlag):
		#Move arm along axis
		#AxisFlag: 0 is base; 1 is shoulder; 2 is elbow; 3 is wrist
		#DirectionFlag: 0 = anticlockwise/up; 1 = clockwise/down
		#convert from axis flag to ArmCmd:
		ArmCmd = self.commands[AxisFlag][DirectionFlag]
		
		#Check movement does not go outside range
		#Current position + timeunits*[in direction -1 or 1]
		if DirectionFlag = 0:
			if (self.positions[AxisFlag] + TimeUnits)>self.ranges[AxisFlag]:
				raise Exception("Movement out of range")
		if DirectionFlag = 1:
			if (self.positions[AxisFlag] - TimeUnits)<0:
				raise Exception("Movement out of range")
				
		# Start the movement
		self.arm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
		# Stop the movement after waiting specified duration
		time.sleep(TimeUnits*self.duration)
		ArmCmd=[0,0,0]
		self.arm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
		
		#record new position
		positiontag = "position_"+AxisFlag
		if DirectionFlag = 0:
			newposition = self.positions[AxisFlag] + TimeUnits
		else:
			newposition = self.positions[AxisFlag] - TimeUnits
		self.positions[AxisFlag] = newposition
		
		#find position tag in config file
		for elem in tree.iterfind(positiontag):
			elem.text = str(newposition)
		tree.write("config.xml)
		
		
	def grip(self, state):
		#Open or close grip
		#state = 0 for close, 1 for open
		if state = 0:
			if self.gripstate = True:
				#Open Grip
				self.arm.ctrl_transfer(0x40,6,0x100,0,[2,0,0],1000)
				time.sleep(0.5)
				ArmCmd=[0,0,0]
				self.arm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
				
				#record new state
				for elem in tree.iterfind("gripstate"):
					elem.text = str(False)
				tree.write("config.xml)
		
		if state = 1:
			if self.gripstate = False:
				#Close Grip
				self.arm.ctrl_transfer(0x40,6,0x100,0,[1,0,0],1000)
				time.sleep(0.5)
				ArmCmd=[0,0,0]
				self.arm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
				
				#record new state
				for elem in tree.iterfind("gripstate"):
					elem.text = str(True)
				tree.write("config.xml)
		
	
	def light(self, state):
		#Turn light on (1) or off (0)
		#MoveArm(1,[0,0,1]) #Light On
		if state = 1:
			self.arm.ctrl_transfer(0x40,6,0x100,0,[0,0,1],1000)
		#MoveArm(1,[0,0,0]) #Light Off
		if state = 0:
			self.arm.ctrl_transfer(0x40,6,0x100,0,[0,0,0],1000)