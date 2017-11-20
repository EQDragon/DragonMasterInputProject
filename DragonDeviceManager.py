import threading
import DragonMasterSerialDevice



###################Debug String Methods########################
"""
Returns a new string that is of the desired length
"""
def set_string_length(string1, lengthOfString, spacingChar = ' '):
    remainingLength = lengthOfString - len(string1)
    newStringToReturn = ''
    if remainingLength > 0:
        newStringToReturn = [spacingChar] * int(remainingLength)
    newStringToReturn = newStringToReturn + string1
    remainingLength = lengthOfString - len(newStringToReturn)
    if remainingLength > 0:
        newStringToReturn += [spacingChar] * remainingLength

    return newStringToReturn


###############################################################


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

        print
        pass

    ########################################################################


"""
Dragon Master Device is the basic foundation that all devices should have when checking for errors and
organizing all the devices to each player station
"""
class DragonMasterDevice:

    def __init__(self, deviceName):
        self.deviceName = deviceName
        self.parentPath = self.get_parent_device_path()

    def get_parent_device_path(self):
        pass


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

