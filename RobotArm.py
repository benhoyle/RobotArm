# import the USB and Time libraries into Python
import usb.core, usb.util, time, thread, os
import elementtree.ElementTree as ET

class Robot:
	def __init__(self):
		# Allocate the name 'RoboArm' to the USB device
		self.arm = usb.core.find(idVendor=0x1267, idProduct=0x0000)
		# Check if the arm is detected and warn if not
		if self.arm is None:
			raise ValueError("Arm not found")
		
		self.commands = [([0,1,0], [0,2,0]), ([64,0,0], [128,0,0]), ([16,0,0], [32,0,0]), ([4,0,0], [8,0,0])]
		self.duration = 0.5 #Period of time units
		self.ranges = []
		self.positions = []
		
		#Load position and range values
		#Check if config file exists
		if os.path.exists('config.xml'):
			#Read XML file
			self.tree = ET.ElementTree(file='config.xml')
		else:
			print("run config") #error - need to run config
		
		#Access ranges tags
		iter_obj = self.tree.getiterator('ranges')
		
		for elem in iter_obj[0].getchildren():
			self.ranges.append(elem.text)
		iter_obj = self.tree.getiterator('positions')
		
		for elem in iter_obj[0].getchildren():
			self.positions.append(elem.text)
			
		print self.ranges, self.positions
		#Access grip_state
		for elem in self.tree.getiterator('gripstate'):
			self.gripstate = elem.text
			
	def move(self, TimeUnits, AxisFlag, DirectionFlag):
		#Move arm along axis
		#AxisFlag: 0 is base; 1 is shoulder; 2 is elbow; 3 is wrist
		#DirectionFlag: 0 = anticlockwise/up; 1 = clockwise/down
		#convert from axis flag to ArmCmd:
		ArmCmd = self.commands[AxisFlag][DirectionFlag]
		
		#Check movement does not go outside range
		#Current position + timeunits*[in direction -1 or 1]
		if DirectionFlag == 0:
			if (int(self.positions[AxisFlag]) + TimeUnits)>int(self.ranges[AxisFlag]):
				raise Exception("Movement out of range")
		if DirectionFlag == 1:
			if (int(self.positions[AxisFlag]) - TimeUnits)<0:
				raise Exception("Movement out of range")
				
		# Start the movement
		self.arm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
		# Stop the movement after waiting specified duration
		time.sleep(TimeUnits*self.duration)
		ArmCmd=[0,0,0]
		self.arm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
		
		#record new position
		positiontag = "position_"+str(AxisFlag)
		if DirectionFlag == 0:
			newposition = int(self.positions[AxisFlag]) + TimeUnits
		else:
			newposition = int(self.positions[AxisFlag]) - TimeUnits
		self.positions[AxisFlag] = str(newposition)
		
		#find position tag in config file
		for elem in self.tree.getiterator(positiontag):
			elem.text = str(newposition)
		self.tree.write("config.xml")
		print self.ranges, self.positions
		
	def grip(self, state):
		#Open or close grip
		#state = 0 for close, 1 for open
		
		if state == 0:
			print "Closing Grip..."
			if self.gripstate == "True":
				#print "."
				#Close Grip
				self.arm.ctrl_transfer(0x40,6,0x100,0,[1,0,0],1000)
				time.sleep(0.6)
				ArmCmd=[0,0,0]
				self.arm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
				print "Grip Closed"
				#record new state
				for elem in self.tree.getiterator("gripstate"):
					elem.text = str(False)
				self.tree.write("config.xml")
				self.gripstate = str(False)
			else:
				print "Grip Already Closed"
		
		if state == 1:
			print "Opening Grip"
			if self.gripstate == "False":
				#print "."
				#Open Grip
				self.arm.ctrl_transfer(0x40,6,0x100,0,[2,0,0],1000)
				time.sleep(0.5)
				ArmCmd=[0,0,0]
				self.arm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
				print "Grip Open"
				#record new state
				for elem in self.tree.getiterator("gripstate"):
					elem.text = str(True)
				self.tree.write("config.xml")
				self.gripstate = str(True)
			else:
				print "Grip Already Open"
		
	
	def light(self, state):
		#Turn light on (1) or off (0)
		#MoveArm(1,[0,0,1]) #Light On
		if state == 1:
			self.arm.ctrl_transfer(0x40,6,0x100,0,[0,0,1],1000)
		#MoveArm(1,[0,0,0]) #Light Off
		if state == 0:
			self.arm.ctrl_transfer(0x40,6,0x100,0,[0,0,0],1000)