import serial
#Serial takes these two parameters: serial device and baudrate
ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    if ser.inWaiting():

        data = ser.readline()
        print(data.decode('utf-8'))

