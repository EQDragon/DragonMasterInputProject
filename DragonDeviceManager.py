import threading
import DragonMasterSerialDevice





class DragonMasterDeviceManager:

    def __init__(self):
        self.deviceList = []
        self.deviceDictionary = {}

    def add_device(self, dragonMasterDevice):
        if not self.deviceDictionary.has_key(dragonMasterDevice.devicePath):

            pass
        self.deviceList.append(dragonMasterDevice)

    def remove_device(self, dragonMasterDevice):
        if not self.deviceDictionary.has_key(dragonMasterDevice.devicePath):

            pass


    #############Contains Methods############################################
    def manager_contains_drax_device(self, draxDevice):
        if draxDevice is not DragonMasterSerialDevice.Draxboard:
            return


        for playerStation in self.deviceDictionary.items():
            if playerStation != None and playerStation.draxboardDevice != None:

                pass

            pass

        return

    def manager_contains_dbv_device(self, dbvDevice):

        return

    def manager_contains_joystick_device(self, joystickDevice):

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