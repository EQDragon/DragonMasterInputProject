import DragonMasterSerialDevice
import DragonDeviceManager
import pygame
import pyudev

context = pyudev.Context

drax1 = DragonMasterSerialDevice.Draxboard('/dev/ttyACM0')
drax1.start_device()
#It is important to initialize pygame before we use it
pygame.init()
pygame.joystick.init()




user_input = raw_input()
while user_input != 'exit':
    user_input = raw_input()
    pass

