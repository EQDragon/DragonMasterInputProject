import DragonMasterSerialDevice
import DragonDeviceManager
import pygame
import pyudev
import os

context = pyudev.Context


#It is important to initialize pygame before we use it
pygame.init()
pygame.joystick.init()

#for dev in pyudev.Context().list_devices():
#   if 'ttyACM0' in dev.device_path.decode('utf-8'):
#      print "Hello"
    #print dev.parent

DragonMasterSerialDevice.print_all_comport_info()


#Initialize an instance of DragonMaster Device Manager that will handle events coming from all DragonMaster devices
dragonMasterDeviceManager = DragonDeviceManager.DragonMasterDeviceManager()




while 1:
	pass

