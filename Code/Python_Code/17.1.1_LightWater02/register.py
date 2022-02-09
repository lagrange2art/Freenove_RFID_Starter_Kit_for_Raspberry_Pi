
import RPi.GPIO as GPIO
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np
import sys




class Register(object):
    def __init__(self, DSpin=11, STpin  = 13, SHpin=15):
    
        """ Define GPIO Pins for register 74HC595
: 
        :param int DSpin: DS Pin of 74HC595(Pin14)
        :param int STpin: ST_CP Pin of 74HC595(Pin12)
        :param int SHpin: CH_CP Pin of 74HC595(Pin11)
        """
        self.DSpin, self.DSstate = DSpin, False
        self.STpin, self.STstate = STpin, False
        self.SHpin, self.SHstate = SHpin, False
    
        GPIO.setmode(GPIO.BOARD)          # use PHYSICAL GPIO Numbering
        GPIO.setup(self.DSpin, GPIO.OUT)  # set pin to OUTPUT mode
        GPIO.setup(self.STpin, GPIO.OUT)
        GPIO.setup(self.SHpin, GPIO.OUT)
          
        self.fig = plt.figure()
        
        regaxis = plt.axes([0.3, 0.3, 0.45, 0.08])
        regaxis.set_xlim([0,9])
        regaxis.set_ylim([0,2])
        regaxis.set_xticks(np.arange(9))
        regaxis.set_yticks(np.arange(2))
        regaxis.set_xticklabels(['' for i in range(9)])
        regaxis.set_yticklabels(['' for i in range(2)])
        regaxis.grid()
        
        self.reg = np.zeros((2,9))  # 1Byte (alias one register) 
        self.regplot = regaxis.imshow(self.reg, extent=(0,9,0,2), interpolation='nearest', cmap=plt.get_cmap('Blues'), vmin=0, vmax=1)
        # reg[0,0]   is virtual register that shows DSstate
        # reg[0,1-8] registers of 74HC595 unit
        # reg[1,1-8] output signals
        
        plt.suptitle('register')

        DSaxis = plt.axes([0.3, 0.75, 0.15, 0.08])         # [left, bottom, width, height]
        self.DSbutton = Button(DSaxis, 'DS %s' % self.DSstate, color='lightgoldenrodyellow', hovercolor='0.975')
        self.DSbutton.on_clicked(self.DS_click)

        SHaxis = plt.axes([0.6, 0.75, 0.15, 0.08])         #
        self.SHbutton = Button(SHaxis, 'SH_CH %s' % self.SHstate, color='lightgoldenrodyellow', hovercolor='0.975')
        self.SHbutton.on_clicked(self.SH_click)

        STaxis = plt.axes([0.45, 0.50, 0.15, 0.08])         
        self.STbutton = Button(STaxis, 'ST_CH %s' % self.STstate, color='lightgoldenrodyellow', hovercolor='0.975')
        self.STbutton.on_clicked(self.ST_click)
        


        releasebutton = plt.axes([0.7, 0.4, 0.15, 0.04])         # button to reset value
        self.release = Button(releasebutton, 'Release GPIO', color='red', hovercolor='0.975')
        self.release.on_clicked(self.destroy)

        plt.show()


    def DS_click(self, event):
        self.DSstate = not self.DSstate
        GPIO.output(self.DSpin, self.DSstate)
        self.DSbutton.label.set_text('DS %s' % self.DSstate)
        
        self.reg[0,0] = self.DSstate
        self.regplot.set_data(self.reg)
        self.fig.canvas.draw_idle()


        
    def SH_click(self, event):
        self.SHstate = not self.SHstate
        GPIO.output(self.SHpin, self.SHstate)
        self.SHbutton.label.set_text('SH %s' % self.SHstate)

        if self.SHstate == 1:
            self.reg[0,1:] = self.reg[0,:-1]
            self.reg[0,0] = self.DSstate
            
            self.regplot.set_data(self.reg)
            self.fig.canvas.draw_idle()

    def ST_click(self, event):
        """ output of regiser"""
        self.STstate = not self.STstate
        GPIO.output(self.STpin, self.STstate)
        self.STbutton.label.set_text('ST %s' % self.STstate)
        
        if self.STstate == True:
            self.reg[1,1:] = self.reg[0,1:]

            self.regplot.set_data(self.reg)
            self.fig.canvas.draw_idle()


    def destroy(self, event):
        print('cleanup')
        GPIO.cleanup()                     # Release all GPIO


def main():
    Register()

if __name__ == '__main__':
    main()
