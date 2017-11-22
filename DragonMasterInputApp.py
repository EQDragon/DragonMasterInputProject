import DragonMasterSerialDevice
import DragonDeviceManager
import pygame
import pyudev

context = pyudev.Context


#It is important to initialize pygame before we use it
pygame.init()
pygame.joystick.init()

#Initialize an instance of DragonMaster Device Manager that will handle events coming from all DragonMaster devices
dragonMasterDeviceManager = DragonDeviceManager.DragonMasterDeviceManager()




user_input = raw_input()
while user_input != 'exit':
    user_input = raw_input()
    pass

