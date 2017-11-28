import threading
import DragonMasterSerialDevice
from time import sleep
import Queue
import pygame
import syslog
import os
import pyudev



class DragonMasterDeviceManager:

    DRAGON_DEVICE_INPUT_TEXT_FILE = "DragonMasterInput.txt"
    DRAGON_DEVICE_OUTPUT_TEXT_FILE = "DragonMasterOutput.txt"
    POLL_TIME_IN_SECONDS = 2

    def __init__(self):
        self.eventQueue = Queue.Queue()
        self.deviceList = []
        self.deviceDictionary = {}
        self.deviceContext = pyudev.Context()


        #Thread for writing to text file
        self.writePollingThread = threading.Thread(target=self.poll_write_to_input_text)
        self.writePollingThread.daemon = True
        self.writePollingThread.start()

        #Thread for polling devices to make sure they are not malfunctioning
        self.debugCommandThread = threading.Thread(target=self.poll_debug_commands)
        self.debugCommandThread.daemon = True
        self.debugCommandThread.start()

        #Thread to poll devices for malfunctions and reconnection
        self.pollDeviceThread = threading.Thread(target=self.poll_devices)
        self.pollDeviceThread.daemon = True
        self.pollDeviceThread.start()
        return


    ######################THREADED METHODS#######################################

    """
    Thread that is used to write all the current events to a text file
    Runs roughly 60 times a second
    """
    def poll_write_to_input_text(self):

        while True:
            self.write_to_text_input()
            sleep(.016)#Wait 1/60 of a second

    """
    Thread that is used to pass in debug commands through the console.
    Probably want to deactivate this functionality in final build....
    """
    def poll_debug_commands(self):

        while True:
            inputLine = raw_input()
            inputLineComponents = inputLine.split()

            if len(inputLineComponents) > 0:
                command = inputLineComponents[0]

                if command == 'status':
                    self.print_all_player_station_status()
                    pass
                elif command == 'help':
                    self.print_help_options()
                elif command == 'reset':
                    if len(inputLineComponents) >= 2:
                        self.debug_reset_dbv(inputLineComponents[1])
                    pass
                elif command == 'idle':
                    if len(inputLineComponents) >= 2:
                        self.debug_idle_dbv(inputLineComponents[1])
                    pass
                elif command == 'inhibit':
                    if len(inputLineComponents) >= 2:
                        self.debug_inhibit_dbv(inputLineComponents[1])
                    pass
                else:
                    print "\'" + command + "\' is not a valid command"
        return


    def poll_devices(self):
        while True:
            self.deviceContext = pyudev.Context() #Want to reinitialize the context of the system at every update
            self.search_devices()
            sleep(2)



    #############################################################################


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
    def search_devices(self):
        #Get All Drax Devices
        DragonMasterSerialDevice.get_all_drax_comports()
        for element in DragonMasterSerialDevice.get_all_drax_comports():
            if element != None and element.device != None:
                if not self.manager_contains_drax_device(element.device):
                    self.add_device(DragonMasterSerialDevice.Draxboard(deviceManager=self, deviceName=element.name, comport=element.device))

        #Get all connected DBV400 devices
        for element in DragonMasterSerialDevice.get_all_dbv400_comports():
            if element != None and element.device != None:
                if not self.manager_contains_dbv_device(element.device):
                    self.add_device(DragonMasterSerialDevice.DBV400(deviceManager=self, deviceName=element.name, comport=element.device))

        for joystick in get_all_joystick_devices():
            if joystick != None and not self.manager_contains_joystick(joystick.get_id()):
                pass


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

    def manager_contains_joystick(self, joystickID):

        for dev in self.deviceList:
            if isinstance(dev, JoystickDevice):
                if dev.joystick.get_id() == joystickID:
                    return True
        return False


    """
    Use this method to check that the Draxboard Device that is being checked does not already exist in
    the manager. Useful to ensure that we do not add duplicate devices
    The parameter that should be passed in should be a string of the Comport for the draxboard
    """
    def manager_contains_drax_device(self, draxDeviceComport):
        if draxDeviceComport == None:
            return False

        for dev in self.deviceList:#REMOVE THIS FOR LOOP WHEN DEVICE DICTIONARY IS ADDED
            if isinstance(dev, DragonMasterSerialDevice.Draxboard):
                if dev.comport == draxDeviceComport:
                    return True

                    
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

        for dev in self.deviceList:#REMOVE THIS FOR LOOP ONCE DEVICE DITIONARY IS ADDED
            if isinstance(dev, DragonMasterSerialDevice.Draxboard):
                if dev.comport == dbvDeviceComport:
                    return True


        for playerStation in self.deviceDictionary.items():
            if playerStation != None and playerStation.dbvDevice != None:
                if playerStation.dbvDevice.comport == dbvDeviceComport:
                    return True

        return False

    """
    Use this method to make sure that the device manager does not already contain an instance of the joystick that
    is currently trying to be added. If there is a duplicate the method will return True.

    TODO: Figure out what parameter to pass in
    """
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
            print inputTextFileInfo.st_size

            


    ########################################################################
    ####################Debug Methods#######################################

    def print_help_options(self):
        print set_string_length("-", lengthOfString=60, spacingChar='-')
        print "Hello! You may enter commands to test various components in the Dragon Master Input Manager"
        print "\'status\' - Prints the status of all the devices currently connected to the machine"
        print "\'idle\' - Enter this command followed by the comport of the DBV400 to set it to the idle state"
        print "\'inhibit\' - Enter this command followed by the comport of the DBV400 to set it to the inhibit state"
        print "\'reset\' - Enter this command followed by the comport of the DBV400 to reset the device. Will be set to idle after reset is complete"
        print set_string_length("-", lengthOfString=60, spacingChar='-')

    def print_all_player_station_status(self):
        pass

    def print_player_station_status(self, playerStationParentDeviceKey):
        if not self.deviceDictionary.has_key(playerStationParentDeviceKey):
            return
        playerStation = self.deviceDictionary[playerStationParentDeviceKey]

        drax = playerStation.draxboardDevice
        dbv = playerStation.dbvDevice
        joy = playerStation.joystickDevice
        pass


    """
    Calls the idle function in the DBV400 device that matches the comport provided
    """
    def debug_idle_dbv(self, dbvDeviceComport):
        for dev in self.deviceList:
            if dev is DragonMasterDeviceManager.DBV400 and dev.comport == dbvDeviceComport:
                dev.idle_dbv()
                return
        return

    """
    Calls the reset function in the DBV400 device that matches the comport provided
    """
    def debug_reset_dbv(self, dbvDeviceComport):
        for dev in self.deviceList:
            if dev is DragonMasterDeviceManager.DBV400 and dev.comport == dbvDeviceComport:
                dev.reset_dbv()
                return
        return

    """
    Calls the inhibiti function in the DBV400 device that matches the comport provided
    """
    def debug_inhibit_dbv(self, dbvDeviceComport):
        for dev in self.deviceList:
            if dev is DragonMasterDeviceManager.DBV400 and dev.comport == dbvDeviceComport:
                dev.inhibit_dbv()
                return

        return



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

    def __init__(self, pygameJoystick):
        DragonMasterDevice.__init__(self)
        self.pygameJoystick = pygameJoystick
        self.joystickID = self.pygameJoystick.get_id()

    """
    Returns a Tuple instance in the format (X-axis, Y-axis) that indicates the current state of the
    joystick. If there is an error reading the joystick, the method will return None
    """
    def get_joystick_axes(self):
        try:
            x = self.pygameJoystick.get_axis(0)
            y = self.pygameJoystick.get_axis(1)

            return (x, y)
        except:
            return None

    def set_parent_device_path(self):
        return


        


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
    JOYSTICK_DEVICE_NAME = "Ultimarc UltraStik Ultimarc Ultra-Stik Player 1"
    joystickList = []
    for j in range(pygame.joystick.get_count()):

        jStick = pygame.joystick.Joystick(j)

        if jStick.get_name() == JOYSTICK_DEVICE_NAME:
            joystickList.append(jStick)

    return joystickList
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
Returns a new string that is of size lengthOfString. Fills the remaining space between string1 and string2
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