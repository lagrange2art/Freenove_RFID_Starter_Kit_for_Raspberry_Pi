#!/usr/bin/env python3
########################################################################
# Filename    : ColorfulLED.py
# Description : Random color change ColorfulLED
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import RPi.GPIO as GPIO
import time
import random

pins = [11, 12, 13]         # define the pins for R:11,G:12,B:13 

def setup(freq):
    global pwmRed,pwmGreen,pwmBlue  
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    GPIO.setup(pins, GPIO.OUT)     # set RGBLED pins to OUTPUT mode
    GPIO.output(pins, GPIO.HIGH)   # make RGBLED pins output HIGH level
    pwmRed = GPIO.PWM(pins[0], freq)      # set PWM Frequence to 2kHz
    pwmGreen = GPIO.PWM(pins[1], freq)  # set PWM Frequence to 2kHz
    pwmBlue = GPIO.PWM(pins[2], freq)    # set PWM Frequence to 2kHz
    pwmRed.start(100)      # set initial Duty Cycle to 0
    pwmGreen.start(100)
    pwmBlue.start(100)

def setColor(r_val,g_val,b_val):      # change duty cycle for three pins to r_val,g_val,b_val
    pwmRed.ChangeDutyCycle(r_val)     # change pwmRed duty cycle to r_val
    pwmGreen.ChangeDutyCycle(g_val)   
    pwmBlue.ChangeDutyCycle(b_val)

def loop():
    while True :
        
        r= 100 - float(input('red: ') or '100')#random.randint(0,100)  #get a random in (0,100)
        g= 100 - float(input('green: ') or '100')#, orrandom.randint(0,100)
        b= 100 - float(input('blue: ') or '100')#random.randint(0,100)
        setColor(r,g,b)          #set random as a duty cycle value 
        print ('r=%d, g=%d, b=%d ' %(r ,g, b))
        time.sleep(1)
        
def destroy():
    pwmRed.stop()
    pwmGreen.stop()
    pwmBlue.stop()
    GPIO.cleanup()
    
if __name__ == '__main__':     # Program entrance
    print ('Program is starting ... ')
    setup(freq=100)
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
