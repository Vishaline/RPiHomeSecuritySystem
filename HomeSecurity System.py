from Adafruit_IO import Client, Feed
from Adafruit_IO import MQTTClient
import RPi.GPIO as GPIO
import picamera


def connect(c):
    c.subscribe(feed_id)
   
def disconnect(c):
    c.unsubscribe(feed_id)

#Setting up the password system
def message(client,feed_id,payload):
    password ='0000'
    global p
    global ep
    p=p+payload
    ep+='*'
    aio.send(lcd_feed.key,ep)
          
    if (payload == '#'):
        if (password+'#' == p) :
            aio.send(lcd_feed.key,"Alarm Off")
            p=''
            ep=''
            GPIO.output(l,False)#LED turns OFF
            client.disconnect()   
        else:
            aio.send(lcd_feed.key,"Wrong Password")
            p=''
            ep=''
            
#Setting up the camera to record video
def cam():
    print("Motion Detected")
    picam.start_preview(alpha=200)
    picam.rotation=180
    picam.capture('cam.jpg',resize=(600,600))
    picam.stop_preview()
    
    picam.resolution = (640, 480)
    picam.start_recording('my_video.h264')
    picam.wait_recording(10)
    picam.stop_recording()
    
    GPIO.output(l,True)#LED turns ONN
    c.connect()
    c.loop_blocking()

l=36#LED
ir=8#IR SENSOR
p=''
ep=''

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(l, GPIO.OUT,initial=GPIO.HIGH)#GPIO=16
GPIO.setup(ir,GPIO.IN) #GPIO=14

ADAFRUIT_IO_USERNAME = "Vish2002"
ADAFRUIT_IO_KEY = "aio_SXuZ39JsWt7mJjaI5T0zD2NoNOvA"

#Connecting to Adafruit
feed_id='key'
c = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
c.on_connect=connect
c.on_disconnect=disconnect
c.on_message =message

#Sending data to Adafruit    
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
cam_feed=aio.feeds('cam')
lcd_feed=aio.feeds('screen')
aio.send(lcd_feed.key,'Temp')

#configuring Pi Camera
picam=picamera.PiCamera()


while True:
    status=GPIO.input(ir)
    #IF MOTION DETECTED
    if (status==0):
        aio.send(lcd_feed.key,"Enter Password: \n#-->enter")
        cam()#START RECORDING
                        
    else:
        GPIO.output(l,False)
