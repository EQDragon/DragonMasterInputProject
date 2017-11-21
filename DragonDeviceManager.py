import threading
import DragonMasterSerialDevice
import inputs
from time import sleep
import pygame
import Queue
import syslog




class DragonMasterDeviceManager:

    def __init__(self):
        self.eventQueue = Queue.Queue()
        self.deviceList = []
        self.deviceDictionary = {}


    """
    Use this method to add a new device to the list of all connected 
    dragon master devices
    """
    def add_device(self, dragonMasterDevice):
        if not self.deviceDictionary.has_key(dragonMasterDevice.devicePath):

            pass
        self.deviceList.append(dragonMasterDevice)

    """
    Use this method to remove currently connected devices. Typically you may want to remove
    malfunctioned devices so that they do not cause problems when polling
    """
    def remove_device(self, dragonMasterDevice):
        if not self.deviceDictionary.has_key(dragonMasterDevice.devicePath):

            pass

    def poll_search_devices(self):
        #Get All Drax Devices
        draxElementList = DragonMasterSerialDevice.get_all_drax_comports()
        for element in draxElementList:
            if element != None and element.port != None:
                pass



    #############Contains Methods############################################

    """
    Use this method to check that the Draxboard Device that is being checked does not already exist in
    the manager. Useful to ensure that we do not add duplicate devices
    The parameter that should be passed in should be a string of the Comport for the draxboard
    """
    def manager_contains_drax_device(self, draxDeviceComport):
        if draxDeviceComport == None:
            return False


        for playerStation in self.deviceDictionary.items():
            if playerStation != None and playerStation.draxboardDevice != None:
                if playerStation.draxboardDevice.comport == draxDeviceComport:
                    return True

        return False

    """
    Use this method to make sure that the device manager does not already contain an instance of this dbv device.
    Useful to ensure that do not add duplicate DBV devices before initializing a new device
    The parameter that should be passed in is a string of the comport for the DBV Device
    """
    def manager_contains_dbv_device(self, dbvDeviceComport):
        if dbvDeviceComport == None:
            return False

        for playerStation in self.deviceDictionary.items():
            if playerStation != None and playerStation.dbvDevice != None:
                if playerStation.dbvDevice.comport == dbvDeviceComport:
                    return True

        return False

    def manager_contains_joystick_device(self, joystickDevice):

        return


    ########################################################################

    ######################EVENT METHODS#####################################
    """
    Writes a new event to a queue that will be written to a text file for later use.
    Use this to write a button event as well as any error events that may occur with the
    device manager
    """
    def add_event_to_queue(self, eventString):
        self.eventQueue.put(eventString)

        return
    ########################################################################
    ####################Debug Methods#######################################

    def print_player_station_status(self, playerStationParentDeviceKey):
        if not self.deviceDictionary.has_key(playerStationParentDeviceKey):
            return
        playerStation = self.deviceDictionary[playerStationParentDeviceKey]

        drax = playerStation.draxboardDevice
        dbv = playerStation.dbvDevice
        joy = playerStation.joystickDevice
        pass

    ########################################################################


"""
Dragon Master Device is the basic foundation that all devices should have when checking for errors and
organizing all the devices to each player station
"""
class DragonMasterDevice:

    def __init__(self):
        self.parentPath = self.get_parent_device_path()

    def get_parent_device_path(self):
        pass


class JoystickDevice(DragonMasterDevice):

    def __init__(self):
        DragonMasterDevice.__init__(self)
        


"""
PlayerStation contains a reference to each device that should be attached to the player station in out cabinet
"""
class PlayerStation:

    def __init__(self, draxboardDevice=None, dbvDevice=None, joystickDevice=None, printerDevice=None, parentDevicePathKey = None):
        self.draxboardDevice = draxboardDevice
        self.dbvDevice = dbvDevice
        self.joystickDevice = joystickDevice
        self.printerDevice = printerDevice
        self.parentDevicePathKey = parentDevicePathKey
        return



###############Device Search Methods###########################
def get_all_joystick_devices():


    for i in range (pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        while 1:
            for event in pygame.event.get():
                print event
                pass
            #print "x: " + str(round(joystick.get_axis(0), 2)) + " y: {} " + str(round(joystick.get_axis(1), 2))


            sleep(.01)




    return
##############################################################


###################Debug String Methods########################
"""
Returns a new string that is of the desired length. Fills in remaining space with
spacingChar value. Make sure that spacingChar is of length 1 if you want accurately spaced
string
"""
def set_string_length(string1, lengthOfString = 60, spacingChar = ' '):
    remainingLength = lengthOfString - len(string1)
    newStringToReturn = ''
    if remainingLength > 0:
        newStringToReturn = spacingChar * int(remainingLength)
    newStringToReturn = newStringToReturn + string1
    remainingLength = lengthOfString - len(newStringToReturn)
    if remainingLength > 0:
        newStringToReturn += spacingChar * remainingLength

    return newStringToReturn

"""
Returns a new string that is of size lenghtOfString. Fills the remaining space between string1 and string2
with the char spacingChar. Please make sure that the variable spacingChar is of length = 1 if you want
accurately sized string.
"""
def set_string_length_multiple(string1, string2, lengthOfString = 60, spacingChar = ' '):
    remainingLength = lengthOfString - len(string1) - len(string2)

    if remainingLength > 0:
        return string1 + (spacingChar * remainingLength) + string2
    else:
        return string1 + string2

###############################################################