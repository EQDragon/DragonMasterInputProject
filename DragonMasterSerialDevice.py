from time import sleep
import serial
import serial.tools.list_ports
import threading
import DragonDeviceManager



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
A safe method to flush the input and output streams of a serial device
"""
def flush_serial_device(dragonMasterSerialDevice):
    serialDevice = dragonMasterSerialDevice.serialDevice
    try:
        serialDevice.flushInput()
        serialDevice.flushOutput()
    except:
        "There was an error flushing serial device " + dragonMasterSerialDevice.to_string()

    return



"""
Use this method if you expect multiple reads to take place after writing to a serial port
This will return a list with the size 'desiredReadCount'

(SerialDevice) dragonMasterSerialDevice: The generic serial device that contains a refernce to the serial port that is going to be read
(int) dataToWrite: The byte array that you want to write to the serial port
(int) minBytesToRead: The minimum bytes on in
"""
def write_serial_device_wait_multiple_read(dragonMasterSerialDevice, dataToWrite, minBytesToRead=1, maxMilisecondsToWaitPerRead=10, delayBeforeReadInMilliseconds = 2, desiredReadCount=2):
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
                readList[i] = read_serial_device(dragonMasterSerialDevice, delayBeforeReadInMilliseconds=delayBeforeReadInMilliseconds)
                break
            sleep(.001)

    dragonMasterSerialDevice.blockReadEvent = False
    return readList


"""
safely writes to a serial port and 
"""
def write_serial_device_wait_for_read(dragonMasterSerialDevice, dataToWrite, minBytesToRead = 1, maxMillisecondsToWait = 10, delayBeforeReadInMilliseconds = 2):
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
            readLine = read_serial_device(dragonMasterSerialDevice, delayBeforeReadInMilliseconds=delayBeforeReadInMilliseconds)
            dragonMasterSerialDevice.blockReadEvent = False
            return readLine
        sleep(.001)
    print (dragonMasterSerialDevice.to_string() + " timed out!")#If write serial device


"""
safely write to a serial port. This method will not return any read values
"""
def write_serial_device(dragonMasterSerialDevice, dataToWrite):
    serialDevice = dragonMasterSerialDevice.serialDevice
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


"""
Polls a serial thread to check if at any point there is something to read from a given serial device
"""
def poll_serial_thread(dragonMasterSerialDevice):
    serialDevice = dragonMasterSerialDevice.serialDevice
    deviceRunning = True
    while deviceRunning:
        try:

            if serialDevice.in_waiting > 1:
                dragonMasterSerialDevice.on_data_received_event()
        except:
            print ("There was an error polling device " + dragonMasterSerialDevice.to_string())
            deviceRunning = False






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


############################## SERIAL CLASSES ###################################
#==================================================================================================================================================
"""
Generic class for all serial devices. Creates an instance and opens a serial port for the proveided
comport
"""
class SerialDevice(DragonDeviceManager.DragonMasterDevice):
    

    def __init__(self, deviceManager, deviceName, comport, baudrate = 9600):
        self.baudrate = baudrate
        self.blockReadEvent = False
        self.deviceFailedStart = False
        self.comport = comport
        self.serialDevice = None
        self.deviceName = deviceName
        self.deviceManager = deviceManager
        DragonDeviceManager.DragonMasterDevice.__init__(self, deviceManager)
        return
        

    """
    This method is called whenever there is bytes_waiting size greater than or equal to 1 byte. You may have to add aditional 
    waits after that to make sure you are reading the entire byte array.
    """
    def on_data_received_event(self):
        pass

    """
    Default start_device begins the polling for any read events that the serial device may trigger
    This will always be called once when the device is first added to the list
    """
    def start_device(self):
        self.serialDevice = open_serial_device(comport=self.comport, baudrate=self.baudrate, readTimeout=3, writeTimeout=5)
        if (self.serialDevice == None):
            self.deviceFailedStart = True

        readPollingThread = threading.Thread(target=poll_serial_thread, args=(self,))
        readPollingThread.daemon = True
        readPollingThread.start()

    """
    This method should be used to obtain the path to the parent device. Ideally this will point to the USB hub that all devices
    for a player station will be connected to
    """
    def set_parent_path(self):
        pass
        
        
    def to_string(self):
        return "SerialDevice (" + self.comport + ")"

    def is_device_connected(self):
        try:
            return self.serialDevice.is_open
        except:
            return False

#=====================================================================================================================================================
"""
A serial device class that handles all functionality with the Drax board

This class should interpret events
"""
class Draxboard(SerialDevice):
    #Contant write bytes. Don't change these variables. They are used to write to the draxboard
    REQUEST_STATUS = bytearray([0x01, 0x00, 0x01, 0x02])
    READ_INPUTS = bytearray([0x03, 0x01, 0x01, 0x05])
    CLEAR_OUTPUTS = bytearray([0x04, 0x02, 0x05, 0x00, 0x00, 0x00, 0x00, 0x0B])
    OUTPUT_DISABLE = bytearray([0x07, 0x03, 0x05, 0xff, 0xff, 0xff, 0xff, 0x0B])
    METER_INCREMENT = bytearray([0x09, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00])

    BYTE_SIZE = 8
    INPUT_BYTE_INDEX = 3




    def __init__(self, deviceManager, deviceName, comport):
        SerialDevice.__init__(self, deviceManager, deviceName, comport, baudrate=115200)
        
        
    """
    In the context of the Drax board, a data received event will primarily be used to collect
    the current status of all the buttons on the board. Any time a button is pressed or released,
    an event will be sent and this will read the current state of each button
    """
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
            if (tempLine[0].encode('hex') == 'fa' and len(tempLine) >= 3):
                self.add_input_event_to_device_manager(tempLine[self.INPUT_BYTE_INDEX].encode('hex'))
        return

    """
    In the context of the Drax board, we much traverse two layers down to reach the USB hub that the board is connected to.
    """
    def set_parent_path(self):

        for dev in self.deviceManager.deviceContext.list_devices():
            if self.deviceName in dev.device_path.decode('utf-8'):
                self.parentPath = dev.parent.parent.parent.device_path
                return
        return
                
    """
    Whenever an event is called we want to send it to the Device Manager to print out the current state of the board,
    which can later be written into a text format for other programs to interpret
    """
    def add_input_event_to_device_manager(self, inputByte):
        inputByteInt = int(inputByte, 16)#inputByte is passed as a hex string. Need to convert to int value.

        inputByteString = ''
        for i in range(self.BYTE_SIZE):
            if inputByteInt & (1 << i) != 0:
                inputByteString += '1'
            else:
                inputByteString += '0'
        print ('DRAX|' + inputByteString + '|' + self.parentPath)



    def to_string(self):
        return "Draxboard (" + self.comport + ")"

    def start_device(self):
        SerialDevice.start_device(self)
        if write_serial_device_wait_for_read(self, self.REQUEST_STATUS) == None:
            self.deviceFailedStart = True
        return

    def increment_meter(self, amountToIncrement, isInMeter):
        if isInMeter:
            self.METER_INCREMENT[3] = 0x00
        else:
            self.METER_INCREMENT[3] = 0x01

        if (amountToIncrement >> 8) == 0:
            self.METER_INCREMENT[4] = amountToIncrement
            self.METER_INCREMENT[6] = self.METER_INCREMENT[0] + self.METER_INCREMENT[1] + self.METER_INCREMENT[2] + self.METER_INCREMENT[3] +\
                                      self.METER_INCREMENT[4] + self.METER_INCREMENT[5]
            write_serial_device(self, self.METER_INCREMENT)



#===============================================================================================================================================
class DBV400(SerialDevice):
    #Variables used for blocking data received events
    INIT = 1
    BUSY = 0
    PASSIVE_RECEIVE = 0

    #COMMANDS
    STATUS_REQUEST = bytearray([0x12, 0x08, 0x00, 0x00, 0x00, 0x10, 0x10, 0x00])
    POWER_ACK = bytearray([0x12, 0x09, 0x00, 0x10, 0x00, 0x81, 0x00, 0x00, 0x06])
    SET_UID = bytearray([0x12, 0x09, 0x00, 0x10, 0x00, 0x20, 0x01, 0x00, 0x01])
    RESET_REQUEST = bytearray([0x12, 0x08, 0x00, 0x10, 0x01, 0x00, 0x11, 0x00])
    INHIBIT_ACK = bytearray([0x12, 0x09, 0x00, 0x10, 0x01, 0x82, 0x00, 0x01, 0x06])
    INHIBIT_REQUEST = bytearray([0x12, 0x08, 0x00, 0x10, 0x01, 0x00, 0x12, 0x00])
    IDLE_REQUEST = bytearray([0x12, 0x08, 0x00, 0x10, 0x01, 0x00, 0x13, 0x10])
    IDLE_ACK = bytearray([0x12, 0x09, 0x00, 0x10, 0x01, 0x83, 0x01, 0x11, 0x06 ])
    ESCROW_ACK = bytearray([0x12, 0x09, 0x00, 0x10, 0x01, 0x85, 0x02, 0x11, 0x06])
    BILL_REJECT = bytearray([0x12, 0x09, 0x00, 0x10, 0x02, 0x80, 0x04, 0x11, 0x06])
    ERROR_ACK = bytearray([0x12, 0x09, 0x00, 0x10, 0x00, 0x80, 0x01, 0x12, 0x06])
    STACK_INHIBIT = bytearray([0x12, 0x08, 0x00, 0x10, 0x02, 0x00, 0x14, 0x10])
    VEND_VALID_ACK = bytearray([0x12, 0x09, 0x00, 0x10, 0x02, 0x86, 0x03, 0x11, 0x06])
    ERROR_ACK = bytearray([0x12, 0x09, 0x00, 0x10, 0x00, 0x80, 0x01, 0x12, 0x06])

    #STATES OF DBV
    IDLE_STATE = "IDLE"
    INHIBIT_STATE = "INHIBIT"
    NOT_INIT_STATE = "NOT INIT"
    UNSUPPORTED_STATE = "UNSUPPORTED"
    POWER_UP_STATE = "POWER UP"
    POWER_UP_NACK_STATE = "POWER UP NACK"
    ERROR_STATE = "ERROR"
    CLEAR_STATE = "CLEAR"

    #UID (ARBITRARY)
    UID = 0x42
    
    def __init__(self, deviceManager, deviceName, comport):
        self.STATE = self.NOT_INIT_STATE
        SerialDevice.__init__(self,deviceManager, deviceName, comport, baudrate=9600)

    def on_data_received_event(self):
      #print('PASS REC = ', +self.PASSIVE_RECEIVE)
      if self.INIT == 0 and self.PASSIVE_RECEIVE == 1:
        read = read_serial_device(self)
    ######################Start If Statements#############################
        if len(read) >= 10 and read[8].encode('hex') == '55' and read[9].encode('hex') == '53' and read[10].encode('hex') == '44':
            denomination = bytearray(read[11])
            write_serial_device(self, self.ESCROW_ACK)
            read = write_serial_device_wait_multiple_read(self, self.STACK_INHIBIT, minBytesToRead=1, maxMilisecondsToWaitPerRead=11000, delayBeforeReadInMilliseconds= 10, desiredReadCount=2)[1]
            if (len(read) >= 8 and read[6].encode('hex') == '04' and read[7].encode('hex') == '11'):
                print('DBV BILL REJECT')
                self.BILL_REJECT[5] = read[5]
                read = write_serial_device_wait_for_read(self, self.BILL_REJECT, 1, 200)
                self.IDLE_ACK[5] = read[5]
                write_serial_device(self, self.IDLE_ACK)
                return
            read = write_serial_device_wait_for_read(self, self.VEND_VALID_ACK, 1, 600)
            print('denomination = ',denomination[0])  # Return denomination here
            if len(read) > 0:
                self.INHIBIT_ACK[5] = read[5]
            read = write_serial_device_wait_for_read(self, self.INHIBIT_ACK, 1, 500)
            if len(read) > 0:
                self.IDLE_ACK[5] = read[5]
            write_serial_device(self, self.IDLE_ACK)
            sleep(.2)
            self.STATE = self.get_state()
        if (len(read) >= 8 and read[6].encode('hex') == '04' and read[7].encode('hex') == '11'):
            print('DBV BILL REJECT')
            self.BILL_REJECT[5] = read[5]
            read = write_serial_device_wait_for_read(self, self.BILL_REJECT, 1, 200)
            self.IDLE_ACK[5] = read[5]
            write_serial_device(self, self.IDLE_ACK)
            return
        if len(read) >= 8 and read[7].encode('hex') == '00' and (read[8].encode('hex') == '00' or read[8].encode('hex') == '00') and read[9].encode('hex') == '01':
            print("REINITIALIZE")
            self.STATUS_REQUEST = bytearray([0x12, 0x08, 0x00, 0x00, 0x00, 0x10, 0x10, 0x00])
            self.RESET_REQUEST[4] = 0x01
            self.INHIBIT_ACK[4] = 0x01
            self.INHIBIT_REQUEST[4] = 0x01
            self.IDLE_REQUEST[4] = 0x01
            self.IDLE_ACK[4] = 0x01
            self.SET_UID[8] = 0x01
            self.start_dbv()
            return
        if len(read) >= 7 and read[6].encode('hex') == '01' and read[7].encode('hex') == '12':
          self.ERROR_ACK[5] = read[5]
          self.ERROR_ACK[6] = read[6]
          self.ERROR_ACK[7] = read[7]
          write_serial_device(self, self.ERROR_ACK)
          print('OP ERROR')
        if len(read) >= 7 and read[6].encode('hex') == '00' and read[7].encode('hex') == '12':
          self.ERROR_ACK[5] = read[5]
          self.ERROR_ACK[6] = read[6]
          self.ERROR_ACK[7] = read[7]
          write_serial_device(self, self.ERROR_ACK)
          self.STATUS_REQUEST = bytearray([0x12, 0x08, 0x00, 0x00, 0x00, 0x10, 0x10, 0x00])
          self.RESET_REQUEST[4] = 0x01
          self.INHIBIT_ACK[4] = 0x01
          self.INHIBIT_REQUEST[4] = 0x01
          self.IDLE_REQUEST[4] = 0x01
          self.IDLE_ACK[4] = 0x01
          self.SET_UID[8] = 0x01
          self.start_dbv()
          return





    def start_device(self):
        SerialDevice.start_device(self)
        self.start_dbv()
        pass

    def to_string(self):
        return "DBV-400(" + self.comport + ")"

    def set_parent_path(self):
        for dev in self.deviceManager.deviceContext.list_devices():
            if self.deviceName in dev.device_path.decode('utf-8'):
                self.parentPath = dev.parent.parent.device_path
                return;

        return 

    ######################DBV Commands#############################
    """
    Resets the dbv-400 device. Once complete, dbv should be in the idle state ready to receive bills
    """

    #def write_serial_device_wait_multiple_read(dragonMasterSerialDevice, dataToWrite, minBytesToRead=1, maxMilisecondsToWaitPerRead=10, delayBeforeReadInMilliseconds = 2, desiredReadCount=2):
    def reset_dbv(self):
        self.PASSIVE_RECEIVE = 0
        flush_serial_device(self)
        readLineList = write_serial_device_wait_multiple_read(self, self.RESET_REQUEST, minBytesToRead = 1, maxMilisecondsToWaitPerRead=5000, delayBeforeReadInMilliseconds=2,  desiredReadCount=3)

        dbvInfoLine = (readLineList[2])#changed to byte array. Not sure if needed
        if dbvInfoLine != None and len(dbvInfoLine) > 5:
            self.INHIBIT_ACK[5] = dbvInfoLine[5]
        write_serial_device(self,self.INHIBIT_ACK)
        flush_serial_device(self)

        if (self.STATE == self.INHIBIT_STATE):
            self.idle_dbv()
        self.STATE = self.get_state()
        self.PASSIVE_RECEIVE = 1
        return

    """
    Will set the associate dbv-400 device into the idle state, DBV can accept bills from this state
    """
    def idle_dbv(self):
        self.PASSIVE_RECEIVE = 0
        readLineList = write_serial_device_wait_multiple_read(self, self.IDLE_REQUEST, minBytesToRead = 1, maxMilisecondsToWaitPerRead=200, desiredReadCount = 2)
        idleInfo = bytearray(readLineList[1])

        self.IDLE_ACK[5] = idleInfo[5]
        flush_serial_device(self)

        write_serial_device(self, self.IDLE_ACK)
        flush_serial_device(self)

        self.STATE = self.get_state()
        self.PASSIVE_RECEIVE = 1
        return

    """
    Will set the associated dbv-400 device into the inhibit state. DBV can not accept bills in this state
    """
    def inhibit_dbv(self):
        self.PASSIVE_RECEIVE = 0
        readLineList = write_serial_device_wait_multiple_read(self, self.INHIBIT_REQUEST, maxMillisecondsToWait = 10, desiredReadCount = 2)
        inhibitInfo = bytearray(readLineList[1])

        self.INHIBIT_ACK[5] = inhibitInfo[5]

        write_serial_device(self, self.INHIBIT_ACK)
        flush_serial_device(self)

        self.STATE = self.get_state()
        self.PASSIVE_RECEIVE = 1
        return

    """
    Initializes a DBV at start-up
    """
    def start_dbv(self):
        self.PASSIVE_RECEIVE = 0
        self.INIT = 1
        flush_serial_device(self)
        self.STATE = self.get_state()
        flush_serial_device(self)

        if self.STATE == self.UNSUPPORTED_STATE:
            self.set_uid()
            self.STATE = self.get_state()

        while self.STATE == self.POWER_UP_NACK_STATE:
            flush_serial_device(self)
            readLine = bytearray(read_serial_device(self, 200))
            if len(readLine) > 0:
                self.POWER_ACK[5] = readLine[5]
            flush_serial_device(self)
            write_serial_device(self, self.POWER_ACK)
            self.STATE = self.get_state()
            self.PASSIVE_RECEIVE = 0

        if self.STATE == self.POWER_UP_STATE:
            self.set_uid()
            write_serial_device(self, self.SET_UID)
            flush_serial_device(self)
            self.reset_dbv()

        if self.STATE == self.INHIBIT_STATE:
            self.idle_dbv()

        if self.STATE == self.CLEAR_STATE:
            self.reset_dbv()
            self.idle_dbv()
            self.STATE = self.get_state()

        if self.STATE == self.ERROR_STATE:
            self.STATUS_REQUEST = bytearray([0x12, 0x08, 0x00, 0x00, 0x00, 0x10, 0x10, 0x00])
        self.INIT = 0
        self.PASSIVE_RECEIVE = 1
        return

    ###############################################################

    def set_uid(self):
        self.RESET_REQUEST[4] = self.UID
        self.INHIBIT_ACK[4] = self.UID
        self.INHIBIT_REQUEST[4] = self.UID
        self.IDLE_REQUEST[4] = self.UID
        self.IDLE_ACK[4] = self.UID
        self.SET_UID[8] = self.UID
        self.STACK_INHIBIT[4] = self.UID
        self.VEND_VALID_ACK[4] = self.UID
        self.ESCROW_ACK[4] = self.UID
        self.ERROR_ACK[4] = self.UID

        self.STATUS_REQUEST[4] = self.UID
        self.STATUS_REQUEST[3] = 0x10


    """
    Returns a string of the current state of the DBV-400 device
    """
    def get_state(self):
        self.PASSIVE_RECEIVE = 0
        currentState = None
        inputBytes = write_serial_device_wait_for_read(self,self.STATUS_REQUEST,1,3000)
        if (len(inputBytes) >= 7 and inputBytes[8].encode('hex') == 'e4' and len(inputBytes) > 8):
            currentState = self.POWER_UP_NACK_STATE
        elif (inputBytes[1].encode('hex') == '0a'):
            currentState = self.POWER_UP_NACK_STATE
        elif (len(inputBytes) > 13 and inputBytes[11].encode('hex') == '00' and inputBytes[12].encode(
                'hex') == '01' and inputBytes[13].encode('hex') == '00'):
            currentState = self.POWER_UP_STATE
        elif (len(inputBytes) >= 8 and inputBytes[8].encode('hex') == 'e2'):
            currentState = self.UNSUPPORTED_STATE
        elif (len(inputBytes) >= 12 and inputBytes[10].encode('hex') == '00' and inputBytes[11].encode(
                'hex') == '01' and inputBytes[12].encode('hex') == '01'):
            currentState = self.INHIBIT_STATE
        elif (len(inputBytes) >= 12 and inputBytes[10].encode('hex') == '01' and inputBytes[11].encode(
                'hex') == '11' and inputBytes[12].encode('hex') == '11'):
            currentState = self.IDLE_STATE
        elif (len(inputBytes) >= 13 and inputBytes[12].encode('hex') == '11' and inputBytes[13].encode('hex') == 'ff'):
            currentState = self.ERROR_STATE
        elif len(inputBytes) >= 12 and inputBytes[10].encode('hex') == '00' and inputBytes[11].encode('hex') == '12' and inputBytes[12].encode('hex') == '11':
            currentState = self.CLEAR_STATE
        print(currentState)
        self.PASSIVE_RECEIVE = 1
        return currentState


################################################################################
