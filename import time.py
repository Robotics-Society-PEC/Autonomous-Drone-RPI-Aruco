import time
import matplotlib.pyplot as plt
from drawnow import*
import serial
val={}
cnt = 0
port = serial.Serial('COM4',115200,timeout=0.5)
plt.ion()
def makeFig() :
    plt.ylim(-1203,1203)
    plt.title('osciloscope')
    plt.grid(True)
    plt.ylabel('data')
    plt.plot(val,'ro-',label='Channel 0')
    plt.legend(loc='lower right')
    while(True):
        port.write(b's')
        if(port.inWaiting()):
            value=port.redline()
            print(value)
            number=int(value)
            print('Channel 0 : {0}'.format(number))
            time.sleep(0.01)
            val.append(int(number))
            drawnow(makeFig)
            plt.pause(.0000001)
            cnt=cnt+1
            if(cnt>50):
                val.pop(0)
                
