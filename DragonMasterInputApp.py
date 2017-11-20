import DragonMasterSerialDevice
import DragonDeviceManager

for draxElement in DragonMasterSerialDevice.get_all_drax_comports():
    draxSerial = DragonMasterSerialDevice.Draxboard(draxElement.device)

print (DragonDeviceManager.set_string_length('Test', lengthOfString=60, spacingChar='-'))
print (DragonDeviceManager.set_string_length_multiple('Hello', 'Goodbye', lengthOfString=60, spacingChar='='))



user_input = raw_input()
while user_input != 'exit':
    user_input = raw_input()
    pass

