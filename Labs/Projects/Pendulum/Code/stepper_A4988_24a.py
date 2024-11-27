""" stepper_A4988 - driver for boards based on the Allegro A4988 chip.

    Extensively modified by
    ProfHuster@GMail.com
    2024-07-20
    - 
"""
from time import sleep_ms

class Stepper:
    """
    Handles  A4988 hardware driver for bipolar stepper motors
    """
    PULSE_RATE = 100
    PULSE_SLEEP_MS = round(500 / PULSE_RATE)
    
    def __init__(self, dir_pin, step_pin, enable_pin):
        self.dir = 1
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.enable_pin = Pin(enable_pin, Pin.OUT)

        self.step_pin.low()
        self.enable_pin.high() # Note actually should be not_enable
        self.dir = 0
        self.dir_pin.low()
        
        self.count = 0
 

    def do_step(self):
        self.step_pin.high()
        sleep_ms(self.PULSE_SLEEP_MS)
        self.step_pin.low()
        sleep_ms(self.PULSE_SLEEP_MS)
        
        self.count += self.dir
        
    def disable(self):
        self.enable_pin.high()

    def enable(self):
        self.enable_pin.low()
    
    def set_dir(self, dir):
        if dir > 0:
            self.dir = 1
        else:
            self.dir = -1

       
if __name__ == '__main__':
    from machine import Pin
    dir_pin = 13
    step_pin = 14
    enable_pin = 15
    step = Stepper(dir_pin, step_pin, enable_pin)
    step.enable()
    print("Move 100")
    for i in range(400):
        step.do_step()
    print("Move -100")
    step.set_dir(-1)
    for i in range(400):
        step.do_step()
    step.disable()