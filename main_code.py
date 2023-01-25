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
from smbus import SMBus
#from i2c_get_dist import *

bus = SMBus(1)




# set range of all sticks
MIN_YAW = 0.3
MAX_YAW = 0.7
MIN_ROLL = 0.45
MAX_ROLL = 0.55
MIN_PITCH = 0.45
MAX_PITCH = 0.55

# channel mapping 
PITCH_CH = 1
ROLL_CH = 0
YAW_CH = 3
AUX_1_CH = 4
AUX_2_CH = 5
AUX_3_CH = 6


#Pramaters related to PID loop and Aruco
MAX_MAGNITUDE = 10000 # absolute value
OBJECT_IN_RADIUS_IN_PIXEL = 25 # IN PIXELS  

KP_ROLL = 15
KI_ROLL = 1
KD_ROLL = 3

KP_PITCH = 15
KI_PITCH = 1
KD_PITCH = 3




FREQ_IN_SEC_OF_PWM_GEN = 0.05 



# starting  values for all axis

yaw_value = 0.5
roll_value = 0.5
pitch_value = 0.5

is_armed = False







# can adjust yaw axis on basis of an edge of the aruco code or the box detected 
# the above would help maybe i dont know 
# may have to implement running average

e_prev_pitch = list(itertools.repeat(0,1000))
e_prev_roll = list(itertools.repeat(0,1000))



def pid_roll(Distance=0):
    # PID has a limiter in it
    e = Distance
    e_prev_roll.insert(0,e)
    del e_prev_roll[len(e_prev_roll)-1]
    P = KP_ROLL*e
    I = KI_ROLL*sum(e_prev_roll)*FREQ_IN_SEC_OF_PWM_GEN # summ of elements of e
    D = KD_ROLL*(e_prev_roll[0]-e_prev_roll[1])/FREQ_IN_SEC_OF_PWM_GEN # previous error - current error

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
    P = KP_PITCH*e
    I = KI_PITCH*sum(e_prev_pitch)*FREQ_IN_SEC_OF_PWM_GEN # summ of elements of e
    D = KD_PITCH*(e_prev_pitch[0]-e_prev_pitch[1])/FREQ_IN_SEC_OF_PWM_GEN # previous error - current error

    Distance_new =  P + I + D
    # print(Distance_new)
    if Distance_new > MAX_MAGNITUDE/2:
        return MAX_MAGNITUDE/2
    elif Distance_new < -MAX_MAGNITUDE/2:
        return -MAX_MAGNITUDE/2
    else:    
        return(Distance_new)




# vel_x_in = 0
# vel_y_in = 0
#this is based on velocity
# def transmit(roll_value , pitch_value , throttle_value):
#     velocity_y = (pitch_value-0.5)*100
#     velocity_x = (roll_value-0.5)*100
#     #print(f'Velocity {velocity_x} , {velocity_y}')
#     global globalvariable.x_obj,globalvariable.y_obj
#     globalvariable.x_obj = globalvariable.x_obj -velocity_x*FREQ_IN_SEC_OF_PWM_GEN
#     globalvariable.y_obj = globalvariable.y_obj -velocity_y*FREQ_IN_SEC_OF_PWM_GEN
#     pass

#this is based on acceleration
# def transmit(roll_value , pitch_value , throttle_value):
#     acc_y = (pitch_value-0.5)*40
#     acc_x = (roll_value-0.5)*40
#     #add velocity limit
#     #print(f'accerlation {acc_x} , {acc_y}')
#     global vel_y_in , vel_x_in
#     globalvariable.x_obj = globalvariable.x_obj - (vel_x_in*FREQ_IN_SEC_OF_PWM_GEN + 0.5*acc_x*FREQ_IN_SEC_OF_PWM_GEN**2)
#     globalvariable.y_obj = globalvariable.y_obj - (vel_y_in*FREQ_IN_SEC_OF_PWM_GEN + 0.5*acc_y*FREQ_IN_SEC_OF_PWM_GEN**2)

#     vel_x = vel_x_in + acc_x*FREQ_IN_SEC_OF_PWM_GEN
#     vel_y = vel_y_in + acc_y*FREQ_IN_SEC_OF_PWM_GEN
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
    

def arm():
    # check with teensy whether it has armed or not at 100 hz or even less as not so much bt / time wastage
    global yaw_value,roll_value,pitch_value
    # check from wire if the drone has armed
    global is_armed
    is_armed = False
    while not is_armed:
        # chec on i2c 
        time.sleep(0.1)
    pwm_generator.servo[PITCH_CH].set_pulse_width_range(1100, 2010)
    pwm_generator.servo[ROLL_CH].set_pulse_width_range(1100, 2010)
    pwm_generator.servo[YAW_CH].set_pulse_width_range(1100, 2010)
    yaw_value = 0.5
    roll_value = 0.5
    pitch_value = 0.5
    


def pick_magnet():
    pwm_generator.servo[AUX_1_CH].angle = 180 #IN1
    pwm_generator.servo[AUX_2_CH].angle = 0 #IN2
    pwm_generator.servo[AUX_3_CH].angle = 180 #EN






def movedrone(x,y):
    global roll_value, pitch_value 
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
        #throttle_value = something 
        print("Object under drone")
        # land 
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
    #pwm_generator.servo[0].angle = 180
    # function used to set the acttuation range of servo
    #pwm_generator.servo[0].actuation_range = 160
    global yaw_value , roll_value , pitch_value 
    roll_value_angle = 180*roll_value
    pitch_value_angle = 180*pitch_value
    throttle_value_angle = 180*throttle_value
    yaw_value_angle = 180* yaw_value

    print(f' y{yaw_value} r{roll_value} p{pitch_value}')
    pwm_generator.servo[PITCH_CH].angle = pitch_value_angle
    pwm_generator.servo[ROLL_CH].angle = roll_value_angle
    pwm_generator.servo[YAW_CH].angle = yaw_value_angle
    pwm_generator.servo[AUX_1_CH].angle = 90
    pwm_generator.servo[AUX_2_CH].angle = 90

def pwm_generate():
    try:
        while True:
            # global globalvariable.x_obj,globalvariable.y_obj
            # get x,y from aruco or color detection
            #print(f'globalvariable.x_obj = {globalvariable.x_obj} globalvariable.y_obj = {globalvariable.y_obj}')
            movedrone(globalvariable.x_obj , globalvariable.y_obj)
            time.sleep(FREQ_IN_SEC_OF_PWM_GEN)
    except KeyboardInterrupt:
        pwm_generator.servo[THROTTLE_CH].angle = 0
        pwm_generator.servo[PITCH_CH].angle = 90
        pwm_generator.servo[ROLL_CH].angle = 90
        pwm_generator.servo[YAW_CH].angle = 90
        pwm_generator.servo[AUX_1_CH].angle = 90
        pwm_generator.servo[AUX_2_CH].angle = 90
        exit()
    except Exception as e:
        pwm_generator.servo[THROTTLE_CH].angle = 0
        pwm_generator.servo[PITCH_CH].angle = 90
        pwm_generator.servo[ROLL_CH].angle = 90
        pwm_generator.servo[YAW_CH].angle = 90
        pwm_generator.servo[AUX_1_CH].angle = 90
        pwm_generator.servo[AUX_2_CH].angle = 90
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
        
        # Create an object named pwm_generator with 16 channel
        pwm_generator = ServoKit(channels=16)
        # function to set the PWM duty cycle range, leave at default value
        pwm_generator.servo[PITCH_CH].set_pulse_width_range(1100, 2010)
        pwm_generator.servo[ROLL_CH].set_pulse_width_range(1100, 2010)
        pwm_generator.servo[YAW_CH].set_pulse_width_range(1100, 2010)
        pwm_generator.servo[AUX_1_CH].set_pulse_width_range(0, 20000)
        pwm_generator.servo[AUX_2_CH].set_pulse_width_range(0, 20000)
        pwm_generator.servo[AUX_3_CH].set_pulse_width_range(0, 20000)
        

        pwm_generator.servo[PITCH_CH].actuation_range = 180
        pwm_generator.servo[ROLL_CH].actuation_range = 180
        pwm_generator.servo[YAW_CH].actuation_range = 180
        pwm_generator.servo[AUX_1_CH].actuation_range = 180
        pwm_generator.servo[AUX_2_CH].actuation_range = 180
        pwm_generator.servo[AUX_3_CH].actuation_range = 180

        # threads
        pwm_generate_and_pid_and_movedrone_thread = threading.Thread(target=pwm_generate)
        
        
        pwm_generate_and_pid_and_movedrone_thread.start()

        while GPIO.input(23) == GPIO.HIGH:

            print(f"PRESS BUTTON , base line = {globalvariable.baseline}")
            # check the arm status
            # print(give_dist())
            # time.sleep(1)
            #arm()?? 
            # if disarms any time then stop threads
            pass
        
        
    
        
        
        aruco_detection2.detectArucoandGetCoordinates()
        pwm_generate_and_pid_and_movedrone_thread.stop()
        GPIO.cleanup()

except KeyboardInterrupt:
    bus.close()
    GPIO.cleanup()
