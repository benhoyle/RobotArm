sudo apt-get upgrade
sudo apt-get install ipython python-opencv python-scipy python-numpy python-setuptools python-pip
sudo pip install https://github.com/sightmachine/SimpleCV/zipball/master
#groups for pi - pi adm dialout cdrom sudo audio video plugdev games users netdev input
sudo useradd robatt
mkdir ~/Code
cd ~/Code
git clone git://github.com/sightmachine/SimpleCV.git
cd SimpleCV
sudo pip install -r requirements.txt
sudo python setup.py develop


#robot arm
sudo nano /etc/udev/rules.d/85-robotarm.rules
#SUBSYSTEM=="usb", ATTRS{idVendor}=="1267", ATTRS{idProduct}=="0000", ACTION=="add", GROUP="plugdev", MODE="0666"

sudo pip install pyusb --upgrade

#espeak
sudo apt-get install espeak #Can use command line from python

#Kinect
sudo apt-get install freenect
#To be able to access the Kinect you need to add yourself to the video group and change the permission on the created device.
#create a file: /etc/udev/rules.d/66-kinect.rules
#Rules for Kinect ####################################################
#SYSFS{idVendor}=="045e", SYSFS{idProduct}=="02ae", MODE="0660",GROUP="video"
#SYSFS{idVendor}=="045e", SYSFS{idProduct}=="02ad", MODE="0660",GROUP="video"
#SYSFS{idVendor}=="045e", SYSFS{idProduct}=="02b0", MODE="0660",GROUP="video"
### END #############################################################

#Viewer
sudo apt-get install guvcview

#VNC
sudo apt-get install tightvncserver
/usr/bin/tightvncserver #runs VNC server

#OpenCV to Camera
sudo apt-get install cmake
#I think the binaries are now available via the following command
sudo apt-get install libopencv-dev #Installed to /usr/include/opencv2/
#for python
sudo apt-get install python-opencv
