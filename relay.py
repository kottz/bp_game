import RPi.GPIO as gpio
import time


def initGPIO():
    gpio.setmode(gpio.BCM)

    gpio.setup(4, gpio.OUT)
    gpio.setup(17, gpio.OUT)
    gpio.setup(27, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    print("hej blabla")


def turnOn(n):
    if(n==0):
        gpio.output(4, gpio.LOW)
    elif (n==1):
        gpio.output(17, gpio.LOW)
    elif (n==2):
        gpio.output(27, gpio.LOW)
    elif (n==3):
        gpio.output(22, gpio.LOW)

def turnAllOn():
    gpio.output(4, gpio.LOW)
    gpio.output(17, gpio.LOW)
    gpio.output(27, gpio.LOW)
    gpio.output(22, gpio.LOW)
    
def turnOff(n):
    if(n==0):
        gpio.output(4, gpio.HIGH)
    elif (n==1):
        gpio.output(17, gpio.HIGH)
    elif (n==2):
        gpio.output(27, gpio.HIGH)
    elif (n==3):
        gpio.output(22, gpio.HIGH)


def turnAllOff():
    gpio.output(4, gpio.HIGH)
    gpio.output(17, gpio.HIGH)
    gpio.output(27, gpio.HIGH)
    gpio.output(22, gpio.HIGH)

def cleanup():
    gpio.cleanup()
#initGPIO()

#i= 0
#stop = 0

#try:
#    while(stop < 10):
#        turnOn(i)
#        time.sleep(2)
#        turnOff(i)
#        i = (i+1) % 4
#        stop += 1
#finally:
#    gpio.cleanup()
