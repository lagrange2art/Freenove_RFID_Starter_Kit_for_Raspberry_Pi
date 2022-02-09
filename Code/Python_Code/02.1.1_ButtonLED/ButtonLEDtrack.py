""" By Tobias Becker. Create circuit of ButtonLED with LED and Button Pin. 
Add an additional button to GPIO23 (pin 16). This is the play button. 
First play a sequence on button and then play this sequence by pressing
play button. \n record track... \n hit Strg-c to exit programm \n

"""

import RPi.GPIO as GPIO
import time
import numpy as np

ledPin = 11       # ledPin in GPIO17 (with 220Ohm)
buttonPin = 12    # buttonPin in GPIO18 (with 10kOhm)
playPin = 16     # second button Pin in GPIO23 (with 10kOhm)

def setup():
    
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPin, GPIO.OUT)   # set ledPin to OUTPUT mode
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set buttonPin to PULL UP INPUT mode
    GPIO.setup(playPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set trackPin to PULL UP INPUT mode


def loop():

    timing = []        # times for which led remains in a status on/off
    status = [0,0]     # save current status and former status                     
    i = 0
    while True:
        if GPIO.input(playPin)==GPIO.HIGH or len(timing)==0:  # no play
            # record track
            if GPIO.input(buttonPin)==GPIO.LOW:    # led pressed 
                GPIO.output(ledPin,GPIO.HIGH)      # turn on led
                print ('led >>> on \r', end='')       
 
                if (status[0] + status[1]) == 1:   # has status changed?
                    timing.append(time.time())     # save time of change
                
                status[i%2] = 1                    # save on status 
                i += 1
            elif GPIO.input(buttonPin)==GPIO.HIGH: # led released
                GPIO.output(ledPin,GPIO.LOW)       # turn off led 
                print ('led <<< off \r', end='')    

                if (status[0] + status[1]) == 1:   # has status changed?
                    timing.append(time.time())     # save time of change 
                
                status[i%2] = 0
                i += 1
        else:
            # play button
            t = np.array(timing) - timing[0]
            seq = np.diff(t)        # sequence for on/off times
            print('going to make sequence: %s ' % (np.round(seq,2)))
            time.sleep(0.5)

            GPIO.output(ledPin, 1)      # turn on led
            time.sleep(seq[0])                  # remain on for ...
            for l in range(len(seq)//2):
                GPIO.output(ledPin, 0)   # turn off led
                time.sleep(seq[1 + 2*l])        # remain off for ...
                
                GPIO.output(ledPin, 1)  # turn on led
                time.sleep(seq[2*(l + 1)])      # remain on for ...
            GPIO.output(ledPin, GPIO.LOW)       # turn off led
           
            timing = []     # delete track
            status = [0,0]  # reset off status
            i = 0

            
def destroy():
    GPIO.output(ledPin, GPIO.LOW)     # turn off led 
    GPIO.cleanup()                    # Release GPIO resource

if __name__ == '__main__':     # Program entrance
    print (__doc__)
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()

