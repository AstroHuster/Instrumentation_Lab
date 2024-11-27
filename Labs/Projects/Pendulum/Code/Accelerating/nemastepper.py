""" nemastepper.py
From https://github.com/jeffmer/micropython-upybbot/blob/master/nemastepper.py

I'm trying to control a robot that has Nema stepper motors, UART to 
communicate with the host and an SSD1306 I2C display.

I'd like the wheels to run as stable and smooth as possible, so I found this 
code: https://github.com/jeffmer/micropython- ... stepper.py

The idea is that a timer is used to execute a stepper callback which is 
executed at a very high frequency and then the callback decided whether 
to send a pulse to a stepper diver board. Every second I also read 
current and voltage from an INA219 board using I2C, display results on 
a display and also send them to UART.

The problem is that every second the motors "stutter" so it seems like 
LCD/UART code has a priority over the timer. My limited understanding was 
that the timer would pause everything else going on, execute, and then 
return control to the main loop, but it seems like as long as the main 
loop is busy the timer is not called or delayed.

"""
import pyb



class Stepper:
    """
    Handles  A4988 hardware driver for bipolar stepper motors
    """

    
    def __init__(self, dir_pin, step_pin, enable_pin):
        self.step_pin = pyb.Pin(step_pin, pyb.Pin.OUT_PP)
        self.dir_pin = pyb.Pin(dir_pin, pyb.Pin.OUT_PP)
        self.enable_pin = pyb.Pin(enable_pin, pyb.Pin.OUT_PP)
        self.enable_pin.high()       
        self.dir = 0
        self.pulserate = 100
        self.count = 0
        self.speed = 0
        self.MAX_ACCEL = 100   #equivallent to 100 x (periodicity of set_speed) usteps/sec/sec
 

    def do_step(self):   # called by timer interrupt every 100us
        if self.dir == 0:
            return
        self.count = (self.count+1)%self.pulserate
        if self.count == 0:
            self.step_pin.high()
            pass
            self.step_pin.low()
        
    def set_speed(self, speed): #called periodically
        if (self.speed - speed) > self.MAX_ACCEL:
            self.speed -= self.MAX_ACCEL
        elif (self.speed - speed)< -self.MAX_ACCEL:
            self.speed+=self.MAX_ACCEL
        else:
            self.speed = speed
        # set direction
        if self.speed>0:
            self.dir = 1
            self.dir_pin.high()
            self.enable_pin.low()       
        elif self.speed<0:
            self.dir = -1
            self.dir_pin.low()
            self.enable_pin.low()       
        else:
            self.dir = 0
        if abs(self.speed)>0:
            self.pulserate = 10000//abs(self.speed)

    def set_off(self):
        self.enable_pin.high()

    def get_speed(self):
        return self.speed
       

                
            
        
            
    


