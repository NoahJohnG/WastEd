# feed data into the arduino
import serial, os

ser = serial.Serial('/dev/cu.usbmodem1141', 9600)


def main():
    data = 0
    while data = get_data():
        ser.write(int_to_byte(data))


def int_to_byte(x):
    if(x ==1):
        return b'1'
    elif(x == 2):
        return  b'2'
    elif(x==3):
        return b'3'
    else:
        return b'0'

def get_data():
    # zachs code
    return 1


