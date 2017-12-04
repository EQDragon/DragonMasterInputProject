import DragonMasterSerialDevice
import DragonDeviceManager
import pygame
import pyudev
import os
from time import sleep

context = pyudev.Context


#It is important to initialize pygame before we use it
#pygame.init()


#for dev in pyudev.Context().list_devices():
	#print dev#dev.device_path.decode('utf-8')


#DragonMasterSerialDevice.print_all_comport_info()

#Initialize an instance of DragonMaster Device Manager that will handle events coming from all DragonMaster devices
#DragonDeviceManager.get_all_printers()
dragonMasterDeviceManager = DragonDeviceManager.DragonMasterDeviceManager()


#joystickList = DragonDeviceManager.get_all_joystick_devices()
#devicePathList = [None] * len(joystickList)
#print len(joystickList)
#for j in joystickList:
#	j.init()
#	for dev in dragonMasterDeviceManager.deviceContext.list_devices():
#		if ("js" + str(j.get_id() + 1)) == dev.sys_name:
#			devicePathList[j.get_id()] = dev.parent.parent.parent.parent.parent.device_path





while True:
	#pygame.joystick.quit()
	#pygame.joystick.init()
	#pygame.event.pump()
	#print pygame.joystick.get_count()
	#for i in range(len(joystickList)):

	#	if devicePathList[i] != None:
	#		print devicePathList[i] + ":  X-" + str(joystickList[i].get_axis(0))

	#sleep(1)
	pass

