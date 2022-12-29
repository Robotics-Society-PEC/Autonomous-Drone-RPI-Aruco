
MAX_THROTLE = 0.6 # all values in percentage 
MIN_YAW = 0.3
MAX_YAW = 0.7
MIN_ROLL = 0.3
MAX_ROLL = 0.7
MIN_PITCH = 0.3
MAX_PITCH = 0.7

MAX_MAGNITUDE = 50 # absolute value
OBJECT_IN_RADIUS_IN_PIXEL = 25 # IN PIXELS  


# can adjust yaw axis on basis of an edge of the aruco code or the box detected 
# the above would help maybe i dont know 



def pid(distance):

    pass

def transmit()
    pass

def movedrone(x,y):
    angle = arctan(y/x) # adjust this for 0 - 360 to remove if else cases
    displacement = sqrt(x**2 + y**2)
    magnitude = pid(displacement)
    roll_value = 0.5
    pitch_value = 0.5
    throtle_value = 0.2

    if displacement < OBJECT_IN_RADIUS_IN_PIXEL:
        # object directly below 
        # start landing 
        #throtle_value = something 
        pass
    elif y>0 and x>0 :
        roll_value = MIN_ROLL + ((magnitude*cos(angle) - (MAX_MAGNITUDE/2))/MAX_MAGNITUDE)*(MAX_ROLL - MIN_ROLL)
        pitch_value = MIN_ROLL + ((magnitude*sin(angle) - (MAX_MAGNITUDE/2))/MAX_MAGNITUDE)*(MAX_PITCH - MIN_PITCH)
        # first quadrant
        pass
    elif y>0 and x<0:
        # second quad
        pass
    elif y<0 and x<0:
        #third quad
        pass
    elif y<0 and x>0:
        #4th quadrant
        pass
    elif x==0 or y ==0:
        #go nowhere 
        pass
    transmit(roll_value , pitch_value , throtle_value)
    return
