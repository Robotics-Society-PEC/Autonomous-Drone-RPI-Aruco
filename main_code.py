import math
import itertools
import time
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import threading
import aruco_detection2
# from globalvariable import globalvariable.x_obj , globalvariable.y_obj
import globalvariable


MAX_THROTLE = 0.6 # all values in percentage 
MIN_YAW = 0.3
MAX_YAW = 0.7
MIN_ROLL = 0.3
MAX_ROLL = 0.7
MIN_PITCH = 0.3
MAX_PITCH = 0.7

MAX_MAGNITUDE = 10000 # absolute value
OBJECT_IN_RADIUS_IN_PIXEL = 25 # IN PIXELS  
Kp = 15
Ki = 1
Kd = 3



# can adjust yaw axis on basis of an edge of the aruco code or the box detected 
# the above would help maybe i dont know 

e_prev = list(itertools.repeat(0,200))
total=0
for ele in range(0,len(e_prev_roll)):
    total = total + e_prev_roll[ele]

def pid_roll(Distance=0):
    # PID has a limiter in it
    e = Distance
    e_prev_roll.insert(0,e)
    del e_prev_roll[len(e_prev_roll)-1]
    P = Kp*e
    I = Ki*sum(e_prev_roll)*time_between_function_call # summ of elements of e
    D = Kd*(e_prev_roll[0]-e_prev_roll[1])/time_between_function_call # previous error - current error

    Distance_new =  P + I + D
    # print(Distance_new)
    if Distance_new > MAX_MAGNITUDE/2:
        return MAX_MAGNITUDE/2
    elif Distance_new < -MAX_MAGNITUDE/2:
        return -MAX_MAGNITUDE/2
    else:    
        return(Distance_new)

def pid(Distance=0):
    # PID has a limiter in it
    e = Distance
    e_prev_pitch.insert(0,e)
    del e_prev_pitch[len(e_prev_pitch)-1]
    P = Kp*e
    I = Ki*sum(e_prev_pitch)*time_between_function_call # summ of elements of e
    D = Kd*(e_prev_pitch[0]-e_prev_pitch[1])/time_between_function_call # previous error - current error

    Distance_new =  P + I + D
    # print(Distance_new)
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






# globalvariable.x_obj = 500
# globalvariable.y_obj = 500 # coordinates of object
vel_x_in = 0
vel_y_in = 0
time_between_function_call = 0.05
#this is based on velocity
# def transmit(roll_value , pitch_value , throtle_value):
#     velocity_y = (pitch_value-0.5)*100
#     velocity_x = (roll_value-0.5)*100
#     #print(f'Velocity {velocity_x} , {velocity_y}')
#     global globalvariable.x_obj,globalvariable.y_obj
#     globalvariable.x_obj = globalvariable.x_obj -velocity_x*time_between_function_call
#     globalvariable.y_obj = globalvariable.y_obj -velocity_y*time_between_function_call
#     pass

#this is based on acceleration
# def transmit(roll_value , pitch_value , throtle_value):
#     acc_y = (pitch_value-0.5)*40
#     acc_x = (roll_value-0.5)*40
#     #add velocity limit
#     #print(f'accerlation {acc_x} , {acc_y}')
#     global globalvariable.x_obj,globalvariable.y_obj,vel_y_in , vel_x_in
#     globalvariable.x_obj = globalvariable.x_obj - (vel_x_in*time_between_function_call + 0.5*acc_x*time_between_function_call**2)
#     globalvariable.y_obj = globalvariable.y_obj - (vel_y_in*time_between_function_call + 0.5*acc_y*time_between_function_call**2)

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
    # print(f"moving to {x} , {y}")
    # if x!=0:
    #     angle = (math.atan(y/x))*180/math.pi
    #     if x<0 and y<0:
    #         angle = angle+180
    #     elif x<0 and y>0:
    #         angle = angle+180
    #     elif x>0 and y>0:
    #         angle = angle
    #     elif x>0 and y<0:
    #         angle = angle + 360
    # else:
    #     if y>0:
    #         angle = 90
    #     elif y<0 :
    #         angle = 270
    #     else:
    #         angle = 0 # correct in future
    #print(f'angle = {angle}')
    # angle = int(angle) # adjust this for 0 - 360 to remove if else cases
    displacement = math.sqrt(x**2 + y**2)
    magnitude_roll = pid_roll(x)
    magnitude_pitch = pid_pitch(y)
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
        print(f'magnitude_roll {magnitude_roll} ,  magnitude_pitch = {magnitude_pitch}')
        roll_value = (MIN_ROLL + MAX_ROLL)/2 + ((magnitude_roll)*(MAX_ROLL - MIN_ROLL))/MAX_MAGNITUDE
        pitch_value = (MIN_PITCH + MAX_PITCH)/2 + ((magnitude_pitch)*(MAX_PITCH - MIN_PITCH))/MAX_MAGNITUDE
    print(f'Roll : {roll_value} Pitch {pitch_value}')
    transmit(roll_value , pitch_value , throtle_value)
    return




def transmit(roll_value , pitch_value , throtle_value):
    # function used to set angle to desierd value
    #kit.servo[0].angle = 180
    # function used to set the acttuation range of servo
    #kit.servo[0].actuation_range = 160

    roll_value_angle = 180*roll_value
    pitch_value_angle = 180*pitch_value
    throtle_value_angle = 180*throtle_value
    


    kit.servo[throttle].angle = 90
    kit.servo[pitch].angle = pitch_value_angle
    kit.servo[roll].angle = roll_value_angle
    kit.servo[yaw].angle = 90
    kit.servo[aux1].angle = 90
    kit.servo[aux2].angle = 90

def pwm_generate():
    print("test")
    try:
        while True:
            # global globalvariable.x_obj,globalvariable.y_obj
            # get x,y from aruco or color detection
            print(f'globalvariable.x_obj = {globalvariable.x_obj} globalvariable.y_obj = {globalvariable.y_obj}')
            movedrone(globalvariable.x_obj , globalvariable.y_obj)
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

# also keep in mind that when to stop making pwm 
#when code crashes or ends
if __name__ == "__main__":

        # variable for the servo driver channel
    throttle = 2
    pitch = 1
    roll = 0
    yaw = 3
    aux1 = 4
    aux2 = 5
    roll_value_angle = 0
    pitch_value_angle = 0
    throtle_value_angle = 0

    # Create an object named kit with 16 channel
    kit = ServoKit(channels=16)
    # function to set the PWM duty cycle range, leave at default value
    kit.servo[throttle].set_pulse_width_range(1100, 2010)
    kit.servo[pitch].set_pulse_width_range(1100, 2010)
    kit.servo[roll].set_pulse_width_range(1100, 2010)
    kit.servo[yaw].set_pulse_width_range(1100, 2010)
    kit.servo[aux1].set_pulse_width_range(1100, 2010)
    kit.servo[aux2].set_pulse_width_range(1100, 2010)
    kit.servo[throttle].actuation_range = 180
    kit.servo[pitch].actuation_range = 180
    kit.servo[roll].actuation_range = 180
    kit.servo[yaw].actuation_range = 180
    kit.servo[aux1].actuation_range = 180
    kit.servo[aux2].actuation_range = 180
    pwm_generate_thread = threading.Thread(target=pwm_generate)
    pwm_generate_thread.start()
    
    aruco_detection2.detectArucoandGetCoordinates()
    pwm_generate_thread.stop()

    
            