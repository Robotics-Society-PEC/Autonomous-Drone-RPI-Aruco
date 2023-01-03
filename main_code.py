import math
import itertools
import time
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import threading
import aruco_detection2



MAX_THROTLE = 0.6 # all values in percentage 
MIN_YAW = 0.3
MAX_YAW = 0.7
MIN_ROLL = 0.3
MAX_ROLL = 0.7
MIN_PITCH = 0.3
MAX_PITCH = 0.7

MAX_MAGNITUDE = 180000 # absolute value
OBJECT_IN_RADIUS_IN_PIXEL = 25 # IN PIXELS  
Kp = 10
Ki = 15
Kd = 40



# can adjust yaw axis on basis of an edge of the aruco code or the box detected 
# the above would help maybe i dont know 

e_prev = list(itertools.repeat(0,200))
total=0
for ele in range(0,len(e_prev)):
    total = total + e_prev[ele]

def pid(Distance=0):
    # PID has a limiter in it
    e = Distance
    e_prev.insert(0,e)
    del e_prev[len(e_prev)-1]
    P = Kp*e
    I = Ki*sum(e_prev)*time_between_function_call # summ of elements of e
    D = Kd*(e_prev[0]-e_prev[1])/time_between_function_call # previous error - current error

    Distance_new =  P + I + D
    print(Distance_new)
    if Distance_new > MAX_MAGNITUDE/2:
        return MAX_MAGNITUDE/2
    elif Distance_new < -MAX_MAGNITUDE/2:
        return -MAX_MAGNITUDE/2
    else:    
        return(Distance_new)

# PID(100,100,5 ,5 )
# PID(100,100,5 ,4 )
# PID(100,100,5 ,3 )
# PID(100,100,5 ,2 )
# PID(100,100,5 ,1 )
# PID(100,100,5 ,0 )
# PID(100,100,5 ,-1)
# PID(100,100,5 ,-2 )






x_obj = 500
y_obj = 500 # coordinates of object
vel_x_in = 0
vel_y_in = 0
time_between_function_call = 0.03
#this is based on velocity
# def transmit(roll_value , pitch_value , throtle_value):
#     velocity_y = (pitch_value-0.5)*100
#     velocity_x = (roll_value-0.5)*100
#     #print(f'Velocity {velocity_x} , {velocity_y}')
#     global x_obj,y_obj
#     x_obj = x_obj -velocity_x*time_between_function_call
#     y_obj = y_obj -velocity_y*time_between_function_call
#     pass

#this is based on acceleration
# def transmit(roll_value , pitch_value , throtle_value):
#     acc_y = (pitch_value-0.5)*40
#     acc_x = (roll_value-0.5)*40
#     #add velocity limit
#     #print(f'accerlation {acc_x} , {acc_y}')
#     global x_obj,y_obj,vel_y_in , vel_x_in
#     x_obj = x_obj - (vel_x_in*time_between_function_call + 0.5*acc_x*time_between_function_call**2)
#     y_obj = y_obj - (vel_y_in*time_between_function_call + 0.5*acc_y*time_between_function_call**2)

#     vel_x = vel_x_in + acc_x*time_between_function_call
#     vel_y = vel_y_in + acc_y*time_between_function_call
#     vel_x_in = vel_x
#     vel_y_in = vel_y
#     print(vel_y_in)
#     print(vel_x_in)
#     MAX_VELOCITY = 10
#     if vel_x_in > MAX_VELOCITY:
#         vel_x_in = MAX_VELOCITY
#     elif vel_x_in < -MAX_VELOCITY:
#         vel_x_in = -MAX_VELOCITY
#     if vel_y_in > MAX_VELOCITY:
#         vel_y_in = MAX_VELOCITY
#     elif vel_y_in < -MAX_VELOCITY:
#         vel_y_in = -MAX_VELOCITY
    

def movedrone(x,y):
    angle = (math.atan(y/x))*180/math.pi
    if x<0 and y<0:
        angle = angle+180
    elif x<0 and y>0:
        angle = angle+180
    elif x>0 and y>0:
        angle = angle
    elif x>0 and y<0:
        angle = angle + 360

    print(f'angle = {angle}')
    angle = int(angle) # adjust this for 0 - 360 to remove if else cases
    displacement = math.sqrt(x**2 + y**2)
    magnitude = pid(displacement)
    roll_value = 0.5
    pitch_value = 0.5
    throtle_value = 0.2

    if displacement < OBJECT_IN_RADIUS_IN_PIXEL:
        # object directly below 
        # start landing 
        # make drone stable using GPS how GPS
        #throtle_value = something 
        print("Object under drone")
        
    elif x==0 or y ==0:
        #go nowhere 
        # this wrong check this
        pass
    else:
        print(f'magnitude {magnitude}')
        roll_value = (MIN_ROLL + MAX_ROLL)/2 + ((magnitude*math.cos(angle))*(MAX_ROLL - MIN_ROLL))/MAX_MAGNITUDE
        pitch_value = (MIN_PITCH + MAX_PITCH)/2 + ((magnitude*math.sin(angle))*(MAX_PITCH - MIN_PITCH))/MAX_MAGNITUDE
    print(f'Roll : {roll_value} Pitch {pitch_value}')
    transmit(roll_value , pitch_value , throtle_value)
    return


    # variable for the servo driver channel
throttle = 0
pitch = 1
roll = 2
yaw = 3
aux1 = 4
aux2 = 5
roll_value_angle = 0
pitch_value_angle = 0
throtle_value_angle = 0

# Create an object named kit with 16 channel
kit = ServoKit(channels=16)
# function to set the PWM duty cycle range, leave at default value
kit.servo[throttle].set_pulse_width_range(1000, 2000)
kit.servo[pitch].set_pulse_width_range(1000, 2000)
kit.servo[roll].set_pulse_width_range(1000, 2000)
kit.servo[yaw].set_pulse_width_range(1000, 2000)
kit.servo[aux1].set_pulse_width_range(1000, 2000)
kit.servo[aux2].set_pulse_width_range(1000, 2000)

def transmit(roll_value , pitch_value , throtle_value):
    # function used to set angle to desierd value
    #kit.servo[0].angle = 180
    # function used to set the acttuation range of servo
    #kit.servo[0].actuation_range = 160

    roll_value_angle = 1.8*roll_value
    pitch_value_angle = 1.8*pitch_value
    throtle_value_angle = 1.8*throtle_value
    


    kit.servo[throttle].angle = throtle_value_angle
    kit.servo[pitch].angle = pitch_value_angle
    kit.servo[roll].angle = roll_value_angle
    kit.servo[yaw].angle = 90
    kit.servo[aux1].angle = 90
    kit.servo[aux2].angle = 90
    



# also keep in mind that when to stop making pwm 
#when code crashes or ends
if __name__ == "__main__":

    aruco_detect_thread = threading.Thread(target=aruco_detection2.detectArucoandGetCoordinates)
    aruco_detect_thread.start()
    try:
        while True:
            # get x,y from aruco or color detection
            print(f'x_obj = {x_obj} y_obj = {y_obj}')
            movedrone(x_obj , y_obj)
            time.sleep(time_between_function_call)
    except KeyboardInterrupt:
        kit.servo[throttle].angle = 0
        kit.servo[pitch].angle = 90
        kit.servo[roll].angle = 90
        kit.servo[yaw].angle = 90
        kit.servo[aux1].angle = 90
        kit.servo[aux2].angle = 90
        exit()
    except Exception as e:
        kit.servo[throttle].angle = 0
        kit.servo[pitch].angle = 90
        kit.servo[roll].angle = 90
        kit.servo[yaw].angle = 90
        kit.servo[aux1].angle = 90
        kit.servo[aux2].angle = 90
        print(e)
        exit()

            