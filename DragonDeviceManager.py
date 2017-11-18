import threading






class DragonMasterDeviceManager:
    ###########################################################
    DRAX_DICTIONARY_INDEX = 0
    DBV_DICTIONARY_INDEX = 1
    JOYSTICK_DICTIONARY_INDEX = 2
    PRINTER_DICTIONARY_INDEX = 3
    ###########################################################

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

    def __init__(self, draxboardDevice=None, dbvDevice=None, joystickDevice=None, printerDevice=None):
        self.draxboardDevice = draxboardDevice
        self.dbvDevice = dbvDevice
        self.joystickDevice = joystickDevice
        self.printerDevice = printerDevice

