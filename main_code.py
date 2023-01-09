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
from i2c_get_dist import *




MAX_THROTLE = 0.6 # all values in percentage 
MIN_YAW = 0.3
MAX_YAW = 0.7
MIN_ROLL = 0.45
MAX_ROLL = 0.55
MIN_PITCH = 0.55
MAX_PITCH = 0.45
HEIGHT = 100
throtle_value = 0
yaw_value=0.5
roll_value=0.5
pitch_value=0.5
descent_rate=0.01 
is_armed = False

MAX_MAGNITUDE = 10000 # absolute value
OBJECT_IN_RADIUS_IN_PIXEL = 25 # IN PIXELS  
Kp = 15
Ki = 1
Kd = 3


ht=3


# can adjust yaw axis on basis of an edge of the aruco code or the box detected 
# the above would help maybe i dont know 

e_prev_pitch = list(itertools.repeat(0,1000))
total=0
for ele in range(0,len(e_prev_pitch)):
    total = total + e_prev_pitch[ele]

e_prev_roll = list(itertools.repeat(0,1000))
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

def pid_pitch(Distance=0):
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
#     global vel_y_in , vel_x_in
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
    

    

e_prev = list(itertools.repeat(0,200))
total=0
for ele in range(0,len(e_prev)):
    total = total + e_prev[ele]

def arm():
    global throtle_value,yaw_value,roll_value,pitch_value
    s1= 0 #input from switch on the quad
    time.sleep(10)
    kit.servo[pitch].set_pulse_width_range(1100, 2080)
    kit.servo[roll].set_pulse_width_range(1000, 2010)
    kit.servo[yaw].set_pulse_width_range(1100, 2080)
    throtle_value = 0
    yaw_value = 1
    roll_value = 0
    pitch_value = 1
    time.sleep(5)
    kit.servo[pitch].set_pulse_width_range(1100, 2010)
    kit.servo[roll].set_pulse_width_range(1100, 2010)
    kit.servo[yaw].set_pulse_width_range(1100, 2010)
    throtle_value = 0
    yaw_value = 0.5
    roll_value = 0.5
    pitch_value = 0.5
    


def pick_magnet():
    kit.servo[aux1].angle = 180 #IN1
    kit.servo[aux2].angle = 0 #IN2
    kit.servo[aux3].angle = 180 #EN




#def go_to_height(ht):
 #   print("now in takeoff")
  #  dist=0 #distance between sonar and the ground in cm
   # global throtle_value
    #while dist != ht:
     #   temp=dist
      #  dist= give_dist()#take input from sonar
       # if dist<=temp:
        #    throtle_value=throtle_value+0.05
        #print (f'throtle = {throtle_value}')
        #time.sleep(0.1)
    #Hover()

def Hover():
    print("now in hover")
    global ht
    dist=0
    global throtle_value, descent_rate
    while True: #put condition for landing zone aruco detected
        dist= give_dist()#take input from sonar
        if dist > 1.1*ht: #take dist input from sonar
            throtle_value=throtle_value-descent_rate
        elif dist < 0.9*ht:
            throtle_value=throtle_value+descent_rate  
            
        if throtle_value>1:
            throtle_value=1
        elif throtle_value<0:
            throtle_value=0
        print (f'throtle = {throtle_value}')
        time.sleep(0.4)
    



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
    global roll_value, pitch_value ,throtle_value
    if not is_armed:
        transmit()
        return

    if x >= 640 and y >= 480 :
        print("Dont Move")
        roll_value = 0.5
        pitch_value = 0.5   
        transmit()
        return
        
    displacement = math.sqrt(x**2 + y**2)
    magnitude_roll = pid_roll(x)
    magnitude_pitch = pid_pitch(y)
    roll_value = 0.5
    pitch_value = 0.5
    

    if displacement < OBJECT_IN_RADIUS_IN_PIXEL:
        # object directly below 
        # start landing 
        # make drone stable using GPS how GPS
        #throtle_value = something 
        print("Object under drone")
        global ht
        ht=80
        transmit()
        
    
    else:
        print(f'magnitude_roll {magnitude_roll} ,  magnitude_pitch = {magnitude_pitch}')
        roll_value = (MIN_ROLL + MAX_ROLL)/2 + ((magnitude_roll)*(MAX_ROLL - MIN_ROLL))/MAX_MAGNITUDE
        pitch_value = (MIN_PITCH + MAX_PITCH)/2 + ((magnitude_pitch)*(MAX_PITCH - MIN_PITCH))/MAX_MAGNITUDE
    print(f'Roll : {roll_value} Pitch {pitch_value}')
    transmit()
    return




def transmit():
    # function used to set angle to desierd value
    #kit.servo[0].angle = 180
    # function used to set the acttuation range of servo
    #kit.servo[0].actuation_range = 160
    global yaw_value , roll_value , pitch_value , throtle_value
    roll_value_angle = 180*roll_value
    pitch_value_angle = 180*pitch_value
    throtle_value_angle = 180*throtle_value
    yaw_value_angle = 180* yaw_value

    print(f't{throtle_value} y{yaw_value} r{roll_value} p{pitch_value}')
    kit.servo[throttle].angle = throtle_value_angle
    kit.servo[pitch].angle = pitch_value_angle
    kit.servo[roll].angle = roll_value_angle
    kit.servo[yaw].angle = yaw_value_angle
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
try:
    if __name__ == "__main__":

            # variable for the servo driver channel
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23,GPIO.IN)
        GPIO.setup(24,GPIO.IN,pull_up_down = GPIO.PUD_UP)
        throttle = 2
        pitch = 1
        roll = 0
        yaw = 3
        aux1 = 4
        aux2 = 5
        aux3 = 6


        # Create an object named kit with 16 channel
        kit = ServoKit(channels=16)
        # function to set the PWM duty cycle range, leave at default value
        kit.servo[throttle].set_pulse_width_range(1050, 2010)
        kit.servo[pitch].set_pulse_width_range(1100, 2010)
        kit.servo[roll].set_pulse_width_range(1100, 2010)
        kit.servo[yaw].set_pulse_width_range(1100, 2010)
        kit.servo[aux1].set_pulse_width_range(0, 20000)
        kit.servo[aux2].set_pulse_width_range(0, 20000)
        kit.servo[aux3].set_pulse_width_range(0, 20000)
        kit.servo[throttle].actuation_range = 180
        kit.servo[pitch].actuation_range = 180
        kit.servo[roll].actuation_range = 180
        kit.servo[yaw].actuation_range = 180
        kit.servo[aux1].actuation_range = 180
        kit.servo[aux2].actuation_range = 180
        kit.servo[aux3].actuation_range = 180



        pwm_generate_and_pid_and_movedrone_thread = threading.Thread(target=pwm_generate)
        

        throtle_thread = threading.Thread(target = Hover)
        
        pwm_generate_and_pid_and_movedrone_thread.start()

        while GPIO.input(23) == GPIO.HIGH:

            print(f"PRESS BUTTON , base line = {globalvariable.baseline}")
            # print(give_dist())
            # time.sleep(1)
            pass
        
        arm()
    
        throtle_thread.start()
        
        
        aruco_detection2.detectArucoandGetCoordinates()
        pwm_generate_and_pid_and_movedrone_thread.stop()
        GPIO.cleanup()

except KeyboardInterrupt:
    kit.servo[throttle].angle = 0
    GPIO.cleanup()
