""" By Tobias Becker: 
Frequency modulation for passive buzzer. Use buzzer circuit diagram of Doorbell
project (Buzzer with 5V on (+)pol and p of pnp transistor on (-)pol, ground 
other p-doped end of transistor to ground. No we can use the middle n-doped
pin of the transistor to open or close current and to produce a buzzing sound
or not. Put the middle n-doped part with an 1kOhm resistor to GPIO17 (=Pin11). 
In this code I put a frequency modulation on GPIO17, in this way the buzzer
sounds differently depending on frequency and and duty cycle (dc). The programm
opens a matplotlib window in which u are free to chose the frequency and 
dc via mouseclick. 

Adjust dc to tune the volume
Adjust fruequency for sound frequency

Before exiting remember to release the GPIO-Pin!"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

import RPi.GPIO as GPIO
import time
import functools

class buzzer(object):
        def __init__(self, buzzerPin, maxfreq, initfreq):
                """ define buzzer pin"""
                self.buzzerPin = buzzerPin     # GPIO17 define buzzerPin
                
                GPIO.setmode(GPIO.BOARD)          # use PHYSICAL GPIO Numbering
                GPIO.setup(buzzerPin, GPIO.OUT)   # set buzzerPin to OUTPUT mode
                
                self.p = GPIO.PWM(buzzerPin, initfreq) # set PWM Frequence to 500Hz
                self.p.start(0)                    # read initial values, other params

                self.fig = plt.figure()
                plt.suptitle('GPIO %d' % buzzerPin)
                ax = plt.axes([0.25, 0.4, 0.65, 0.5])                 # [left, bottom, width, height]
                ax.set_ylim([-0.1,1.1])
                ax.set_xlim([0,100])
                ax.set_ylabel('percentage of frequency cycle')
                x = np.linspace(0, 100, 200)
                y = np.zeros_like(x)
                self.line, = ax.plot(x, y)                # plot line to be updated


                scrollbar = plt.axes([0.25, 0.25, 0.65, 0.03],          # [left, bottom, width, height]
                                     facecolor='lightgoldenrodyellow')  # scrollbar for value
                self.slider = Slider(scrollbar, label='dc [percentage]', valmin=0.,
                                     valmax=100.0, valinit=0)           # link scrollbar to slider
                self.slider.on_changed(self.update)                     # update slider when value is changed

                freqbar = plt.axes([0.25, 0.15, 0.65, 0.03],          # [left, bottom, width, height]
                                     facecolor='lightgoldenrodyellow')  # scrollbar for value
                self.freqslider = Slider(freqbar, label='frequency [Hz]', valmin=0,
                                     valmax=maxfreq, valinit=initfreq)           # link scrollbar to slider
                self.freqslider.on_changed(self.update)                     # update slider when value is changed


                resetaxis = plt.axes([0.8, 0.025, 0.1, 0.04])         # button to reset value
                self.resetbutton = Button(resetaxis, 'Reset', color='green', hovercolor='0.975')
                self.resetbutton.on_clicked(self.reset)

                releasebutton = plt.axes([0.5, 0.025, 0.15, 0.04])         # button to reset value
                self.release = Button(releasebutton, 'Release GPIO', color='red', hovercolor='0.975')
                self.release.on_clicked(self.destroy)

                plt.show()


        def reset(self, event):
                """reset value of slider to initial value
                :param event: dummy dependency
                :return:
                """
                print('reset')
                self.p.ChangeFrequency(500)
                self.freqslider.reset()
                
                self.p.ChangeDutyCycle(0)    
                self.slider.reset()


        def update(self, val):
                """
                when dc or frequency is changed
                """
                freq = self.freqslider.val   # frequency for buzzer
                dc = self.slider.val         # dc value for buzzer
                
                self.p.ChangeFrequency(freq) # update frequency
                self.p.ChangeDutyCycle(dc)   # update dc value
                
                x = self.line.get_data()[0]  # array [0,100] 
                y = np.ones_like(x)        
                y[x >= dc] = 0               # dc is fraction of frequency cycle
                self.line.set_ydata(y)
                
                self.fig.canvas.draw_idle()
        


        
        def destroy(self, event):
                print('cleanup')
                GPIO.cleanup()                     # Release all GPIO


def main():
    print(__doc__)
    buzzer(buzzerPin=11, maxfreq=1000, initfreq=500)

if __name__ == '__main__':
    main()
