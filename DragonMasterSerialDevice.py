from time import sleep
import serial
import serial.tools.list_ports
import threading



##########################Serial Functions##########################################
"""
Opens a new serial port and returns that object if successful
If the device failed to open correctly it will return a None object
"""
def open_serial_device(comport, baudrate, readTimeout, writeTimeout):
    try :
        s = serial.Serial(
            port=comport,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
            timeout=readTimeout,

            writeTimeout=writeTimeout
        )
        return s
    except(OSError, serial.SerialException):
        print ('There was an error opening port ' + comport + '. Please make sure you have provided the correct permissions')
        return None


def close_serial_device(serialDevice):
    if (serialDevice == None):
        return

    if (serialDevice.isOpen):
        try:
            serialDevice.close()
        except:
            print("There was an error closing the port")


"""
Use this method if you expect multiple reads to take place after writing to a serial port
This will return a list with the size 'desiredReadCount'

(SerialDevice) dragonMasterSerialDevice: The generic serial device that contains a refernce to the serial port that is going to be read
(int) dataToWrite: The byte array that you want to write to the serial port
(int) minBytesToRead: The minimum bytes on in
"""
def write_serial_device_wait_multiple_read(dragonMasterSerialDevice, dataToWrite, minBytesToRead=1, maxMilisecondsToWaitPerRead=10, desiredReadCount=2):
    readList = [None] * desiredReadCount

    dragonMasterSerialDevice.blockReadEvent = True

    serialDevice = dragonMasterSerialDevice.serialDevice

    try:
        serialDevice.write(dataToWrite)


    except:
        print ("There was an error writing to " + dragonMasterSerialDevice.to_string())
        dragonMasterSerialDevice.blockReadEvent = False
        return readList

    for i in range(desiredReadCount):
        for _ in range(maxMilisecondsToWaitPerRead):
            if serialDevice.in_waiting >= minBytesToRead:
                readList[i] = read_serial_device(dragonMasterSerialDevice)
                break
            sleep(.001)

    dragonMasterSerialDevice.blockReadEvent = False
    return readList


"""
safely writes to a serial port and 
"""
def write_serial_device_wait_for_read(dragonMasterSerialDevice, dataToWrite, minBytesToRead = 1, maxMillisecondsToWait = 10):
    dragonMasterSerialDevice.blockReadEvent = True

    serialDevice = dragonMasterSerialDevice.serialDevice

    try:
        serialDevice.write(dataToWrite)

    except:
        print ("There was an error writing to " + dragonMasterSerialDevice.to_string())
        dragonMasterSerialDevice.blockReadEvent = False
        return


    for _ in range(maxMillisecondsToWait):
        if (serialDevice.in_waiting >= minBytesToRead):
            dragonMasterSerialDevice.blockReadEvent = False
            return read_serial_device(dragonMasterSerialDevice)
        sleep(.001)
    print (dragonMasterSerialDevice.to_string() + " Timed Out")


"""
safely write to a serial port. This method will not return any read values
"""
def write_serial_device(serialDevice, dataToWrite):

    if serialDevice == None or not serialDevice.is_open:
        return

    try:
        serialDevice.write(dataToWrite)

    except:
        print ('There was an error writing to the device ' + serialDevice.port)



"""
safely read from a serial device 
"""
def read_serial_device(dragonMasterSerialDevice, delayBeforeReadInMilliseconds = 0):
    sleep(float(delayBeforeReadInMilliseconds) / 1000)
    serialDevice = dragonMasterSerialDevice.serialDevice
    try:
        readLine = serialDevice.read(size=serialDevice.in_waiting)
        return readLine
    except:
        print ('There was an error reading ' + serialDevice.port)
        return None


def poll_serial_thread(dragonMasterSerialDevice):
    serialDevice = dragonMasterSerialDevice.serialDevice
    while True:
        if serialDevice.in_waiting > 1:
            dragonMasterSerialDevice.on_data_received_event()






####################################################################################


#############################Retrieve Comport Elements##############################
"""
Retireves a collection of all DBV400 devices that are currently attached to this computer

This returns a list of serial elements
"""
def get_all_dbv400_comports():
    allPorts = serial.tools.list_ports.comports()

    dbvComportElements = []
    for element in allPorts:
        if (element.description.__contains__("DBV-400")):
            dbvComportElements.append(element)

    return dbvComportElements


"""
Retrieves a collection of all Draxboard devices that are currently attached to this computer

This returns a list of serial elements
"""
def get_all_drax_comports():
    allPorts = serial.tools.list_ports.comports()

    draxComportElements = []
    for element in allPorts:
        if (element.description.__contains__("Dual RS-232 Emulation - CDC-ACM 1")):
            draxComportElements.append((element))

    return draxComportElements
#########################################################################################


def print_all_comport_info():
    allPorts = serial.tools.list_ports.comports()

    for element in allPorts:
        print (element.serial_number)
        print (element.location)
        print (element.description)
        print (element.device)
        print (element.hwid)
        print (element.interface)
        print (element.serial_number)
        print (element.manufacturer)
        print (element.name)
        print (element.pid)
        print (element.vid)
        print ("---------------------------------------------------")


##############################SERIAL CLASSES###################################
"""
Generic class for all serial devices. Creates an instance and opens a serial port for the proveided
comport
"""
class SerialDevice:
    

    def __init__(self, comport, bauderate = 9600):
        self.blockReadEvent = False
        self.deviceFailedStart = False
        self.comport = comport
        self.serialDevice = open_serial_device(comport=self.comport, baudrate=bauderate, readTimeout=3, writeTimeout=5)
        if (self.serialDevice == None):
            self.deviceFailedStart = True


    def on_data_received_event(self):
        pass

    """
    Default start_device begins the polling for any read events that the serial device may trigger
    """
    def start_device(self):
        readPollingThread = threading.Thread(target=poll_serial_thread, args=(self,))
        readPollingThread.daemon = False
        readPollingThread.start()
        

    def to_string(self):
        return "SerialDevice (" + self.comport + ")"

    def is_device_connected(self):
        try:
            return self.serialDevice.is_open
        except:
            return False


class Draxboard(SerialDevice):
    #Contant write bytes. Don't change these variables. They are used to write to the draxboard
    REQUEST_STATUS = bytearray([0x01, 0x00, 0x01, 0x02])
    READ_INPUTS = bytearray([0x03, 0x01, 0x01, 0x05])
    CLEAR_OUTPUTS = bytearray([0x04, 0x02, 0x05, 0x00, 0x00, 0x00, 0x00, 0x0B])
    OUTPUT_DISABLE = bytearray([0x07, 0x03, 0x05, 0xff, 0xff, 0xff, 0xff, 0x0B])




    def __init__(self, comport):
        SerialDevice.__init__(self, comport, bauderate=115200)

        if self.deviceFailedStart:
            return
        self.start_device()
        
        

    def on_data_received_event(self):
        #Make sure to block data received if you are writing and expecting a read after

        if self.blockReadEvent:
            return

        readBlockSize = 9
        readLine = read_serial_device(self, 0)
        if readLine == None:
            return

        for i in range(int(len(readLine) / readBlockSize)):
            tempLine = readLine[i*readBlockSize:((i+1)*readBlockSize)]
            if (tempLine[0].encode('hex') == 'fa'):
                print (tempLine[3].encode('hex'))






    def to_string(self):
        return "Draxboard (" + self.comport + ")"

    def start_device(self):
        SerialDevice.start_device(self)
        print (write_serial_device_wait_for_read(self, self.REQUEST_STATUS))



class DBV400(SerialDevice):

    STATUS_REQUEST = bytearray([0x12, 0x08, 0x00, 0x00, 0x00, 0x10, 0x10, 0x00])
    POWER_ACK = bytearray([0x12, 0x09, 0x00, 0x10, 0x00, 0x81, 0x00, 0x00, 0x06])
    SET_UID = bytearray([0x12, 0x09, 0x00, 0x10, 0x00, 0x20, 0x01, 0x00, 0x01])
    RESET_REQUEST = bytearray([0x12, 0x08, 0x00, 0x10, 0x01, 0x00, 0x11, 0x00])
    INHIBIT_ACK = bytearray([0x12, 0x09, 0x00, 0x10, 0x01, 0x82, 0x00, 0x01, 0x06])
    INHIBIT_REQUEST = bytearray([0x12, 0x08, 0x00, 0x10, 0x01, 0x00, 0x12, 0x00])
    IDLE_REQUEST = bytearray([0x12, 0x08, 0x00, 0x10, 0x01, 0x00, 0x13, 0x10])
    IDLE_ACK = bytearray([0x12, 0x08, 0x00, 0x10, 0x01, 0x00, 0x13, 0x10])

    def __init__(self, comport):
        SerialDevice.__init__(self, comport, bauderate=9600)

    def on_data_received_event(self):
        pass

    def start_device(self):
        pass

    def get_state(self, inputBytes):
        currentState = None
        if (len(inputBytes) >= 7 and inputBytes[8].encode('hex') == 'e4' and len(inputBytes) > 8):
            currentState = 'POWER UP NACK'
        elif (inputBytes[1].encode('hex') == '0a'):
            currentState = 'POWER UP NACK'
        elif (len(inputBytes) > 13 and inputBytes[11].encode('hex') == '00' and inputBytes[12].encode(
                'hex') == '01' and inputBytes[13].encode('hex') == '00'):
            currentState = 'POWER UP'
        elif (len(inputBytes) >= 8 and inputBytes[8].encode('hex') == 'e2'):
            currentState = 'UNSUPPORTED'
        elif (len(inputBytes) >= 12 and inputBytes[10].encode('hex') == '00' and inputBytes[11].encode(
                'hex') == '01' and inputBytes[12].encode('hex') == '01'):
            currentState = 'INHIBIT'
        elif (len(inputBytes) >= 12 and inputBytes[10].encode('hex') == '01' and inputBytes[11].encode(
                'hex') == '11' and inputBytes[12].encode('hex') == '11'):
            currentState = 'IDLE'
        print(currentState)
        return currentState


################################################################################