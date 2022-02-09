"""by Tobias Becker"""
import RPi.GPIO as GPIO
import time
import numpy as np

note_chart_freq = dict(B5=987.77, C6=1046.5, Cs6=1108.73, D6=1174.66, 
                     Ds6=1244.51, E6=1318.51, F6=1396.91,
                     Fs6=1479.98, G6=1567.98, Gs6=1661.22,
                     A6=1760.00, As6=1864.66, B6=1975.53,
                     C7=2093.00)
                     
    
                

class buzzer(object):
    def __init__(self, buzzerPin):
        """ define buzzer pin"""
        self.buzzerPin = buzzerPin     # GPIO17 define buzzerPin
        
        GPIO.setmode(GPIO.BOARD)          # use PHYSICAL GPIO Numbering
        GPIO.setup(buzzerPin, GPIO.OUT)   # set buzzerPin to OUTPUT mode
        
        self.p = GPIO.PWM(buzzerPin, 1) # set PWM Frequence to 1Hz
        self.p.start(1) 
        
    def loop(self):
        while True:
            freq = float(input('frequency: ') or '1')
            self.p.ChangeFrequency(freq) 
    
    def linsweep(self, freqmin, freqmax, dc=1, duration=10):
        self.p.ChangeDutyCycle(dc)
        freqs = np.linspace(freqmin, freqmax, 100)
        #signal = np.concatenate((x, x[1:-1][::-1]))# 100*np.sin(np.linspace(0,np.pi, 200))
        while True:
            for freq in freqs:
                print('freq: %.2f \r' % freq, end='')
                self.p.ChangeFrequency(freq)#self.p.ChangeDutyCycle(signal[i])
                time.sleep(duration/2/len(freqs))
            for freq in freqs[::-1]:
                print('freq: %.2f \r' % freq, end='')
                self.p.ChangeFrequency(freq)#self.p.ChangeDutyCycle(signal[i])
                time.sleep(duration/2/len(freqs))
    
            
    def play_melody(self, melody, dc=50):
        notes, duration = melody
        while True:
            for i in range(len(notes)):
                freq = note_chart_freq[notes[i]]
                print('tone %s' % notes[i])
                if freq == 'p':
                    self.p.ChangeDutyCycle(0)
                else:
                    self.p.ChangeDutyCycle(dc)
                    self.p.ChangeFrequency(freq)
                time.sleep(duration[i])
                self.p.ChangeDutyCycle(0)
                time.sleep(1/32)

    
    def destroy(self):
        print('cleanup')
        GPIO.cleanup()                     # Release all GPIO
        
def setup():
    global p
    GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
    GPIO.setup(buzzerPin, GPIO.OUT)   # set buzzerPin to OUTPUT mode
        
    p = GPIO.PWM(buzzerPin, 100) # set PWM Frequence to 500Hz
    p.start(0) # set initial Duty Cycle to 0


if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    buzz = buzzer(buzzerPin = 11)
    try:
        #buzz.loop()
        #buzz.linsweep(freqmin=500,freqmax=1000, dc=99, duration=1)
        melody = [['Fs6', 'Fs6', 'D6', 'B5', 'B5', 'E6', 
        'E6', 'E6', 'Gs6', 'Gs6', 'A6', 'B6', 'A6', 'A6', 'A6', 'E6', 'D6', 
        'Fs6', 'Fs6', 'Fs6', 'E6', 'E6', 'Fs6', 'E6'], 
        1./np.array([8, 8, 8, 4, 4, 4, 4, 5, 8, 8, 8, 8, 8, 8, 8, 4, 4, 4, 
        4, 5, 8, 8, 8, 8])]
    
        buzz.play_melody(melody, dc=50)
        
        
        
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        buzz.destroy()

