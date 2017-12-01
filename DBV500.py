import serial
import time
import binascii
from time import sleep
from binascii import hexlify

class dbv500:
     STATUS_REQUEST = ([0x12, 0x08, 0x00, 0x00, 0x00, 0x10, 0x10, 0x00])
     POWER_ACK = ([0x12, 0x09, 0x00, 0x10, 0x00, 0x81, 0x00, 0x00, 0x06])
     SET_UID = ([0x12, 0x09, 0x00, 0x10, 0x00, 0x20, 0x01, 0x00, 0x01]);
     RESET_REQUEST =([0x12, 0x08, 0x00, 0x10, 0x01, 0x00, 0x11, 0x00]);
     INHIBIT_ACK = ([0x12, 0x09, 0x00, 0x10, 0x01, 0x82, 0x00, 0x01, 0x06])
     INHIBIT_REQUEST = ([0x12, 0x08, 0x00, 0x10, 0x01, 0x00, 0x12, 0x00])
     IDLE_REQUEST = ([0x12, 0x08, 0x00, 0x10, 0x01, 0x00, 0x13, 0x10])
     IDLE_ACK = ([0x12, 0x09, 0x00, 0x10, 0x01, 0x83, 0x01, 0x11, 0x06])
     UID = 0x42
     port = serial.Serial('/dev/ttyACM0')
     port.baudrate = 9600
     port.write_timeout = 3
     port.read_timeout = 2
     STATE = 'NOT INIT'

     def Set_UID(self):
         self.RESET_REQUEST[4] = self.UID
         self.INHIBIT_ACK[4] = self.UID
         self.INHIBIT_REQUEST[4] = self.UID;
         self.IDLE_REQUEST[4] = self.UID;
         self.IDLE_ACK[4] = self.UID;
         self.SET_UID[8] = self.UID
         self.STATUS_REQUEST[4] = self.UID
         self.STATUS_REQUEST[3] = 0x10


     def getState(self):
            self.port.write(self.STATUS_REQUEST)
            sleep(.5)
            input_bytes = self.port.read(self.port.inWaiting())
            CURRENT_STATE = 'NONE'
            #print("input = "+input_bytes.encode('hex'))
            if (len(input_bytes) >= 7 and input_bytes[8].encode('hex') == 'e4' and len(input_bytes) > 8):
                CURRENT_STATE = 'POWER UP NACK'
            elif (input_bytes[1].encode('hex') == '0a'):
                CURRENT_STATE = 'POWER UP NACK'
            elif (len(input_bytes) > 13 and input_bytes[11].encode('hex') == '00' and input_bytes[12].encode('hex') == '01' and input_bytes[13].encode('hex') == '00'):
                CURRENT_STATE = 'POWER UP'
            elif (len(input_bytes) >= 8 and input_bytes[8].encode('hex') == 'e2'):
                CURRENT_STATE = 'UNSUPPORTED'
                self.UID = input_bytes[4]
            elif (len(input_bytes) >= 12 and input_bytes[10].encode('hex') == '00' and input_bytes[11].encode('hex') == '01' and input_bytes[12].encode('hex') == '01'):
                CURRENT_STATE = 'INHIBIT'
            elif (len(input_bytes) >= 12 and input_bytes[10].encode('hex') == '01' and input_bytes[11].encode('hex') == '11' and input_bytes[12].encode('hex') == '11'):
                CURRENT_STATE = 'IDLE'
            print(CURRENT_STATE)
            return CURRENT_STATE

     def Reset(self):
         # Reset starts Here
         print('RESET')
         self.port.write(self.RESET_REQUEST)
         time.sleep(.4)
         read = self.port.read(self.port.in_waiting)
         self.port.flushInput()
         self.port.flushOutput()
         while (self.port.in_waiting <= 0):
             pass
         read = self.port.read(self.port.inWaiting())
         self.INHIBIT_ACK[5] = read[5]
         self.port.write(self.INHIBIT_ACK)
         self.port.flushInput()
         self.port.flushOutput()
         STATE = self.getState()
         if(STATE == 'INHIBIT'):
             self.Idle()
         #Reset ends here

     def Idle(self):
         self.port.write(self.IDLE_REQUEST)
         sleep(.005)
         read = self.port.read(9)
         read = self.port.read(9)
         temp_read = bytearray(read)

         self.IDLE_ACK[5] = temp_read[5]
         self.port.write(self.IDLE_ACK)

         self.port.flushInput()
         self.port.flushOutput()

         self.getState()
     def Inhibit(self):
         self.port.write(self.INHIBIT_REQUEST)
         sleep(.005)
         read = self.port.read(9)
         read = self.port.read(9)
         temp_read = bytearray(read)

         self.INHIBIT_ACK[5] = temp_read[5]

         self.port.write(self.INHIBIT_ACK)

         self.port.flushInput()
         self.port.flushOutput()
         self.getState()


     def Start(self):
        print('starting!')
        if (self.port.is_open == False):
            self.port.open()
        self.port.flushInput()
        self.port.flushOutput()
        STATE = self.getState()
        self.port.flushOutput()
        self.port.flushInput()
        if STATE == 'UNSUPPORTED':
            self.Set_UID()
            STATE = self.getState()

        while STATE == 'POWER UP NACK':          #Bill Acceptor has just turned on or needs to be reinitialized
            self.port.flushInput()
            self.port.flushOutput()
            sleep(.5)
            read = self.port.read(self.port.in_waiting)
            self.POWER_ACK[5] = read[5]
            self.port.flushInput()
            self.port.flushOutput()
            self.port.write(self.POWER_ACK)
            time.sleep(.5)
            STATE = self.getState()

        if STATE == 'POWER UP':                  #Bill Acceptor has successfully received ACK from Host
            self.Set_UID()
            self.port.write(self.SET_UID)
            self.port.flushInput()
            self.port.flushOutput()
            self.Reset()

        if STATE == 'INHIBIT':
            self.Idle()

      print('done')
    #End Inhibit to Idle

test = dbv500()
test.Start()



