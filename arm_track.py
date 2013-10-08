from SimpleCV import Camera, Display

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

cam = Camera()

disp = Display(cam.getImage().size())

#Get centre of field of vision
centre = []
centre.append(cam.getImage().size()[0]/2)
centre.append(cam.getImage().size()[0]/2)

while disp.isNotDone():
	img = cam.getImage()
	# Look for a face
	faces = img.findHaarFeatures('face')
	if faces is not None:
		# Get the largest face
		faces = faces.sortArea()
		bigFace = faces[-1]
		# Draw a green box around the face
		bigFace.draw()
		face_location = bigFace.coordinates()
		print face_location, centre
		offset =  (face_location[0] - centre[0])/float(200) #/cam.getImage().size()[0]
		if offset < 0:
			print "clockwise", offset
			MoveArm(abs(offset),[0,2,0]) #Rotate base clockwise
			time.sleep(abs(offset))
		else:
			print "anticlockwise", offset
			MoveArm(abs(offset),[0,1,0]) #Rotate base anticlockwise
			time.sleep(abs(offset))
		
	img.save(disp)
