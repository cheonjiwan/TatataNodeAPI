import RPi.GPIO as GPIO
import time
import requests
import socketio
import numpy as np
import warnings
import math
warnings.filterwarnings('ignore')

sio = socketio.Client()
sio.connect('http://13.124.113.190:8080')
GPIO.setmode(GPIO.BCM)
CPin = [12,16,20,21]

beforep = np.array([2,0])#set the initial view
# it should set first about where the cctv watching now by gps.


for pin in CPin:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,False)
        
        
#left
seq = [ [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]]
#right        
seq2 = [ [1,0,0,1],[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,1,1,0],[0,1,0,0],[1,1,0,0],[1,0,0,0]]


@sio.on('turnCCTV')
def trun_cctv(data):
    direction = data['data']
    
    if direction == 1: #right
        beforep[0] = beforep[0]*(math.cos(math.radians(330)))
        beforep[1] = beforep[1]*(math.sin(math.radians(330)))
        for i in range(22):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(CPin[pin], seq2[halfstep][pin])
                    time.sleep(0.001)

    if direction == 0:
        beforep[0] = beforep[0]*(math.cos(math.radians(30)))
        beforep[1] = beforep[1]*(math.sin(math.radians(30)))
        for i in range(22):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(CPin[pin], seq[halfstep][pin])
                    time.sleep(0.001)
    
    
pos = 0
def calculate_angle(before, after):
       """ Calculate angle between two points """
       zeropoint = np.array([0,0])# cctv gps value
       point_b = zeropoint -before 
       point_a =zeropoint -after 
       ang_a = np.arctan2(*point_a[::-1])
       ang_b = np.arctan2(*point_b[::-1])
       return np.rad2deg((ang_a - ang_b) % (2 * np.pi))
    
@sio.on('sendGPS')
def my_event(data):
    global pos
    global beforep
    print('Recevied data: ', data)

    tolng = data['data']['lng'] # x
    tolat = data['data']['lat'] # y

    tolng = (tolng*100000)%1000
    tolat = (tolat*100000)%1000

    
    afterp = np.array([tolng,tolat])
    topos = int(calculate_angle(beforep, afterp))
    beforep = afterp
    topos *= 1.4

    if topos == -1:
        GPIO.cleanup()

    tmp = pos-topos

    if tmp > 0:
        direction = 0 
    else:
        direction = 1
    tmp = abs(tmp)
    if tmp > 256:
        tmp = 512 - tmp
        if direction == 1:
            direction = 0
        else:
            direction = 1


    if direction == 1:
        for i in range(abs(tmp)):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(CPin[pin], seq2[halfstep][pin])
                    time.sleep(0.001)
    
    if direction == 0:
        for i in range(abs(tmp)):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(CPin[pin], seq[halfstep][pin])
                    time.sleep(0.001)
    pos = topos    
