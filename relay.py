import RPi.GPIO as gpio

PIN1 = 4
PIN2 = 17
PIN3 = 27
PIN4 = 22

def initGPIO():
    gpio.setmode(gpio.BCM)

    gpio.setup(PIN1, gpio.OUT)
    gpio.setup(PIN2, gpio.OUT)
    gpio.setup(PIN3, gpio.OUT)
    gpio.setup(PIN4, gpio.OUT)
    
    turnAllOff()

def turnOn(n):
    if(n==0):
        gpio.output(PIN1, gpio.LOW)
    elif (n==1):
        gpio.output(PIN2, gpio.LOW)
    elif (n==2):
        gpio.output(PIN3, gpio.LOW)
    elif (n==3):
        gpio.output(PIN4, gpio.LOW)

def turnAllOn():
    gpio.output(PIN1, gpio.LOW)
    gpio.output(PIN2, gpio.LOW)
    gpio.output(PIN3, gpio.LOW)
    gpio.output(PIN4, gpio.LOW)
    
def turnOff(n):
    if(n==0):
        gpio.output(PIN1, gpio.HIGH)
    elif (n==1):
        gpio.output(PIN2, gpio.HIGH)
    elif (n==2):
        gpio.output(PIN3, gpio.HIGH)
    elif (n==3):
        gpio.output(PIN4, gpio.HIGH)


def turnAllOff():
    gpio.output(PIN1, gpio.HIGH)
    gpio.output(PIN2, gpio.HIGH)
    gpio.output(PIN3, gpio.HIGH)
    gpio.output(PIN4, gpio.HIGH)

def cleanup():
    gpio.cleanup()
