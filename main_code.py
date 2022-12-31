import math
import itertools

MAX_THROTLE = 0.6 # all values in percentage 
MIN_YAW = 0.3
MAX_YAW = 0.7
MIN_ROLL = 0.3
MAX_ROLL = 0.7
MIN_PITCH = 0.3
MAX_PITCH = 0.7

MAX_MAGNITUDE = 50 # absolute value
OBJECT_IN_RADIUS_IN_PIXEL = 25 # IN PIXELS  
Kp = 50
Ki = 50
Kd = 50

# can adjust yaw axis on basis of an edge of the aruco code or the box detected 
# the above would help maybe i dont know 

e_prev = list(itertools.repeat(0,100))
total=0
for ele in range(0,len(e_prev)):
    total = total + e_prev[ele]

def pid(Distance=0):
    e = Distance
    e_prev.insert(0,e)
    del e_prev[100]
    P = Kp*e
    I = Ki*sum(e_prev) # summ of elements of e
    D = Kd*(e_prev[0]-e_prev[1]) # previous error - current error

    Distance_new =  P + I + D
    print(Distance_new)
    return(Distance_new)

# PID(100,100,5 ,5 )
# PID(100,100,5 ,4 )
# PID(100,100,5 ,3 )
# PID(100,100,5 ,2 )
# PID(100,100,5 ,1 )
# PID(100,100,5 ,0 )
# PID(100,100,5 ,-1)
# PID(100,100,5 ,-2 )








def transmit():
    pass

def movedrone(x,y):
    angle = math.atan(y/x)
    angle = int(angle % 360) # adjust this for 0 - 360 to remove if else cases
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
        pass
    elif x==0 or y ==0:
        #go nowhere 
        pass
    else:
        roll_value = MIN_ROLL + ((magnitude*math.cos(angle) - (MAX_MAGNITUDE/2))/MAX_MAGNITUDE)*(MAX_ROLL - MIN_ROLL)
        pitch_value = MIN_ROLL + ((magnitude*math.sin(angle) - (MAX_MAGNITUDE/2))/MAX_MAGNITUDE)*(MAX_PITCH - MIN_PITCH)
    
    transmit(roll_value , pitch_value , throtle_value)
    return
