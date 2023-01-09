from smbus import SMBus
import time
import globalvariable

# ultrasonic_addr = 32
# bus = SMBus(1)
# distance = 0


# def give_dist():
#     global distance

#     try:

#         distance = int(bus.read_byte(ultrasonic_addr))# have to read 2 ./ 4 bytes 
#         print(f'distance :{distance}')
#     except KeyboardInterrupt:
#         exit()
#     except Exception as e:
#         print(f'Error occured while measuring distance')
#         distance=400
#     return distance
from bmp280 import BMP280
# Initialise the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus, i2c_addr= 0x77)

baseline_values = []
baseline_size = 50

print("""relative-altitude.py - Calculates relative altitude from pressure.

    Press Ctrl+C to exit!

    """)

    

print("Collecting baseline values for {:d} seconds. Do not move the Drone!\n".format(baseline_size))

for i in range(baseline_size):
    pressure = bmp280.get_pressure()
    baseline_values.append(pressure)
    print(i)
    time.sleep(1)

globalvariable.baseline = sum(baseline_values[:-25]) / len(baseline_values[:-25])

def give_dist():
    
    altitude = bmp280.get_altitude(qnh=globalvariable.baseline)
    print('Relative altitude: {:05.2f} metres'.format(altitude))
    return altitude


if __name__ == "__main__":
    while True:

        print(give_dist())
        time.sleep(1)