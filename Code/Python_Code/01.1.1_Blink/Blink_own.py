#!/usr/bin/env python3
########################################################################
# Filename    : Blink.py
# Description : Basic usage of GPIO. Let led blink.
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
import time
import numpy as np

ledPin = 11    # define ledPin

def setup():
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPin, GPIO.OUT)   # set the ledPin to OUTPUT mode
    GPIO.output(ledPin, GPIO.LOW)  # make ledPin output LOW level 
    print ('using pin%d'%ledPin)

def loop():
    while True:
        seq = [0.2, 0.5, 0.2, 0.2]#blinkseq()
        for i in range(len(seq) - 1):

            GPIO.output(ledPin, GPIO.HIGH)  # turn on led
            time.sleep(seq[i])              # remain on for ...
            GPIO.output(ledPin, GPIO.LOW)   # turn off led
            time.sleep(seq[i+1])               # remain off for ...

def destroy():
    GPIO.cleanup()                      # Release all GPIO


def blinkseq(inputseq=['long','short']):
    base = 1.
    short = base/2
    longs = base*2
    
    inputseq = np.array(inputseq)
    outseq = np.ones(len(inputseq))
    outseq[inputseq == 'long'] = longs
    outseq[inputseq == 'short'] = short

    return outseq
    

if __name__ == '__main__':    # Program entrance
    print ('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()

