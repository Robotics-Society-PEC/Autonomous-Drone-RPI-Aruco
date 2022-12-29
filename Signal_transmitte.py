# To download library run "sudo pip3 install adafruit-circuitpython-servokit"
# Import the servo driver library 
from adafruit_servokit import ServoKit

# variable for the servo driver channel
throttle = 0
pitch = 1
roll = 2
yaw = 3
aux1 = 4
aux2 = 5

# Create an object named kit with 16 channel
kit = ServoKit(channels=16)

# function used to set angle to desierd value
#kit.servo[0].angle = 180
# function used to set the acttuation range of servo
#kit.servo[0].actuation_range = 160

# function to set the PWM duty cycle range, leave at default value
kit.servo[throttle].set_pulse_width_range(1000, 2000)
kit.servo[pitch].set_pulse_width_range(1000, 2000)
kit.servo[roll].set_pulse_width_range(1000, 2000)
kit.servo[yaw].set_pulse_width_range(1000, 2000)
kit.servo[aux1].set_pulse_width_range(1000, 2000)
kit.servo[aux2].set_pulse_width_range(1000, 2000)

While(1):
        kit.servo[throttle].angle = 0
        kit.servo[pitch].angle = 90
        kit.servo[roll].angle = 90
        kit.servo[yaw].angle = 90
        kit.servo[aux1].angle = 90
        kit.servo[aux2].angle = 90
        