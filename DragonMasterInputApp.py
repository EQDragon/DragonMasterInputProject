import DragonMasterSerialDevice
import DragonDeviceManager
import pygame
import pyudev

context = pyudev.Context

#It is important to initialize pygame before we use it
pygame.init()
pygame.joystick.init()




user_input = raw_input()
while user_input != 'exit':
    user_input = raw_input()
    pass

