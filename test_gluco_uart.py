import serial
import re

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1.5)
print(ser.name)
get_data = False
raw_data = []
while not get_data:
    if ser.inWaiting() != 0 :
        # Garbage input serial b'/x00/
        msg = ser.read()
        if msg != b'\x00'  : 
            raw_data.append(ser.readlines())
            raw_data.append(ser.readlines())
            print("s1 adalah {}".format(raw_data[0]))
            print("s2 adalah {}".format(raw_data[1]))
            get_data = True

ser.close()
'''
raw_data  = [[a,b],[]]

raw_data[0] = [a,b]
raw_data[0][0] = a

for i in range(len(raw_data))
    if raw_data[i] is not []:
        for j in range(len(raw_data)):
            raw_data[i][j].decode("utf-8")
'''

print("raw_data is {}".format(raw_data[0]))

decoded_string = []

for index in range(len(raw_data)):
    if raw_data[index] is not [] :
        for j in range(len(raw_data[index])):   
            decoded_string.append(raw_data[index][j].decode('ISO-8859-1'))

for i in range(len(decoded_string)):
    print(decoded_string[i])


''' 
TODO : 
- search match string TotalValue 
- if yes , cut string total value - end of string
- then split by space, take fifth element

FIXME has been solved
'''

output = None
for i in range(len(decoded_string)):
    if 'TotalValue' in decoded_string[i]:
        output = re.findall(r'TotalValue.+?(?=0\r)' , decoded_string[i])

final_output = output[0].split(' ')

print(final_output)

print("Gula darah : {}".format(final_output[4]))

'''
TODO : 
add to flow to ke sistem besar
'''
# blood_glucose_clean = re.findall(r'TotalValue.*', blood_glucose_raw)
# clean_measure = blood_glucose_clean.replace('\x00','').split('\r')
# print(blood_glucose_clean)
