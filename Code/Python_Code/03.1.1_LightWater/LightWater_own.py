""" By Tobias Becker. Flowing water light with potentiometer to control
speed."""

import RPi.GPIO as GPIO
from ADCDevice import *
import time

ledPins = [11, 12, 13, 15, 16, 18, 22, 29, 32,  24]
#     GPIO 17, 18, 27, 22, 23, 24, 25,  5, 12, CEO
adc = ADCDevice() # Analog-Digital-Converter


def setup():    
    GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPins, GPIO.OUT)   # set all ledPins to OUTPUT mode
    GPIO.output(ledPins, 1) # make all ledPins output HIGH level, turn off all led


    global adc
    if(adc.detectI2C(0x4b)): # Detect the ads7830 wired to SDA1 SCL1
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)

def loop():
    while True:
        v = max(1, adc.analogRead(0) )
        print ('led speed : %d : \r' % v, end='')

        for pin in ledPins:      # make led(on) move from left to right
            GPIO.output(pin, 0)  # turn on
            v = max(1,adc.analogRead(0))    
            print ('led speed : %d : \r' %v, end='')
            time.sleep(1/v)
            GPIO.output(pin, 1)
            
        for pin in ledPins[::-1]:       # make led(on) move from right to left
            GPIO.output(pin, 0)  
            v = max(1,adc.analogRead(0))    
            print ('led speed : %d : \r' %v, end='')
            time.sleep(1/v)
            GPIO.output(pin, 1)

def destroy():
    GPIO.cleanup()                     # Release all GPIO
    adc.close()
    
if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()

