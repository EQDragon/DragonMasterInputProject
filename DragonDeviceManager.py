import threading
import DragonMasterSerialDevice
import inputs
from time import sleep
import pygame
import Queue
import syslog
import os




class DragonMasterDeviceManager:

    DRAGON_DEVICE_INPUT_TEXT_FILE = "DragonMasterInput.txt"
    DRAGON_DEVICE_OUTPUT_TEXT_FILE = "DragonMasterOutput.txt"

    def __init__(self):
        self.eventQueue = Queue.Queue()
        self.deviceList = []
        self.deviceDictionary = {}

        self.poll_search_devices()




    """
    Use this method to add a new device to the list of all connected 
    dragon master devices
    """
    def add_device(self, dragonMasterDevice):
        if dragonMasterDevice == None:
            return#Don't add a device if it is null
        self.deviceList.append(dragonMasterDevice)
        dragonMasterDevice.start_device()
        print dragonMasterDevice.to_string() + " has been added!"

    """
    Use this method to remove currently connected devices. Typically you may want to remove
    malfunctioned devices so that they do not cause problems when polling
    """
    def remove_device(self, dragonMasterDevice):
        if dragonMasterDevice == None:
            return

        return

    """
    Searches for all valid dragon master devices to add to the device manager. Polls for 
    Draxboard, DBV-400, Joysticks, and Ticket Printers
    """
    def poll_search_devices(self):
        #Get All Drax Devices
        draxElementList = DragonMasterSerialDevice.get_all_drax_comports()
        for element in draxElementList:
            if element != None and element.device != None:
                if not self.manager_contains_drax_device(element.device):
                    self.add_device(DragonMasterSerialDevice.Draxboard(element.device))

        #Get all connected DBV400 devices
        for element in DragonMasterSerialDevice.get_all_dbv400_comports():
            if element != None and element.device != None:
                if not self.manager_contains_dbv_device(element.device):
                    self.add_device(DragonMasterSerialDevice.DBV400(element.device))


        return

    """
    Polls all attached devices and checks if there are any malfunctions among any of the devices.
    Will remove any device that is currently malfunctioned
    """
    def poll_malfunctioned_devices(self):
        for dragonMasterDevice in self.deviceList:
            if dragonMasterDevice:
                pass

        return

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

    """
    Writes all the current events in self.eventQueue to text file to be read in by
    other programs
    """
    def write_to_text_input(self):
        if self.eventQueue.qsize() > 0:
            inputTextFileInfo = os.stat(self.DRAGON_DEVICE_INPUT_TEXT_FILE)
            


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