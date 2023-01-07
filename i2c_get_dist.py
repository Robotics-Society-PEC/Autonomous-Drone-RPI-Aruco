from smbus import SMBus
import time

ultrasonic_addr = 32

while True:
    bus = SMBus(1)
    print(bus.read_byte_data(ultrasonic_addr , 2))# have to read 2 ./ 4 bytes 
    time.sleep(0.01)