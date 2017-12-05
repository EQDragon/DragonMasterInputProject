import DragonMasterSerialDevice
import DragonDeviceManager
import pygame
import pyudev
import os
from time import sleep

#context = pyudev.Context



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

