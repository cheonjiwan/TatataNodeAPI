import RPi.GPIO as GPIO
import time
import requests
import socketio
import serial
#from socketIO_client import SocketIO

URL = "http://tatataserver-env.eba-dbnecqy8.ap-northeast-2.elasticbeanstalk.com/gps"
button = 6
buzzer = 13
count=0
scale = [261,294,329,349,392,440,493,523]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(button, GPIO.IN,GPIO.PUD_UP) # button
GPIO.setup(buzzer, GPIO.OUT) #buzzer
p=GPIO.PWM(buzzer,100)
port = "/dev/ttyS0"
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

# def on_connect():
#     print('connect')

# def on_disconnect():
#     print('disconnect')

# def on_reconnect():
#     print('reconnect')

# def on_send_response(*args):
#     print('on_send_response',args)

def doRequest():
    data = ser.readline()
	#if data.find("$GNGGA")!=-1:
	data = data.decode()
	if data.find("$GNGGA") != -1:
		str = data.split(",")
		print(str[2],str[3],str[4],str[5])
    userInfo = {'success':True,'lng':float(str[4])/100,'lat':float(str[2])/100,'device_id':12345}
    sio.emit('sendGPS',userInfo)

    
def main():
    try:
        while True:
            while True:
                if GPIO.input(button) == 0:
                    count=count+1
                    print(count)
                    if(count>20000):
                        p.start(100)
                        p.ChangeDutyCycle(90)

                        doRequest()
                        print('After doRequest()')
                        time.sleep(2)
                        for i in range(8):
                            print(i+1)
                            p.ChangeFrequency(scale[i])
                            time.sleep(1)
                        p.stop()
                        break
                else:
                    count=0
                    #print("no")
                    time.sleep(1)
            
            #p.stop()

    finally:
        GPIO.cleanup
        

# socketIO = SocketIO('13.124.113.190',8080)
# socketIO.on('connect',on_connect)
# socketIO.on('disconnect',on_disconnect)
# socketIO.on('reconnect',on_reconnect)

# #Listen
# socketIO.on('sendGPS',on_send)

sio = socketio.Client()
sio.connect('http://13.124.113.190:8080')
#sio.wait()
print(f'my sid : {sio.sid}')

@sio.on('sendGPS')
def my_event(data):
    print('Received data: ', data)

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error():
    print("the connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

main()

