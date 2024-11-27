""" stepper_A4988 - driver for boards based on the Allegro A4988 chip.

    Extensively modified by
    ProfHuster@GMail.com
    2024-07-20
    - 24b direct pin values, made code more consise.
"""
from time import sleep_ms
from machine import Pin

N_STEPS = 100

class Stepper:
    """
    Handles  A4988 hardware driver for bipolar stepper motors
    """
    PULSE_RATE = 30
    PULSE_SLEEP_MS = round(500 / PULSE_RATE)
    
    def __init__(self, dir_pin=13, step_pin=14, enable_pin=15, rate=30):
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.enable_pin = Pin(enable_pin, Pin.OUT)

        self.step_pin(0)
        self.disable() # Note actually should be not_enable
        self.set_dir()
        self.set_rate(rate)
        
        self.count = 0
 

    def do_steps(self, n=0):
        print("n= ", n)
        if n >= 0:
            print("Dir 1")
            self.dir_pin(1)
            dn = 1
        else:
            print("Dir 0")
            self.dir_pin(0)
            dn = -1
        for _ in range(abs(n)):       
            self.step_pin(1)
            sleep_ms(self.PULSE_SLEEP_MS)
            self.step_pin(0)
            sleep_ms(self.PULSE_SLEEP_MS)
            self.count += dn
        
    def disable(self):
        self.enable_pin(1)

    def enable(self):
        self.enable_pin(0)
    
    def set_dir(self, dir=1):
        if dir:
            self.dir_pin(1)
        else:
            self.dir_pin(0)
    
    def set_rate(self, rate=100):
        self.PULSE_RATE = rate
        self.PULSE_SLEEP_MS = round(500 / self.PULSE_RATE)        

def test():      
    dir_pin = 13
    step_pin = 14
    enable_pin = 15
    crane = Stepper(rate=500)
    crane.enable()
    print("N_STEPS = ", N_STEPS)
    
    print("Move N_STEPS")
    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
    crane.do_steps(N_STEPS)
    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
        
    sleep_ms(2_000)
    
    print("Move -N_STEPS")
    crane.dir_pin(0)
    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
    crane.do_steps(-N_STEPS)
    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
        
    sleep_ms(2_000)
    
    print("Move N_STEPS")
    crane.dir_pin(1)
    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
    crane.do_steps(N_STEPS)
    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
        
    sleep_ms(2_000)
    
    print("Move -N_STEPS")
    crane.set_dir(0)
    crane.dir_pin(0)
    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
    crane.do_steps(-N_STEPS)
    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
    sleep_ms(2_000)

    print("Move N_STEPS")
    crane.dir_pin(1)
    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
    crane.do_steps(N_STEPS)
    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
    crane.disable()

    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
    print("Done")

    print("Move N_STEPS")
    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
    crane.do_steps(N_STEPS)
    print("crane: ", crane.dir_pin(), crane.step_pin(),
          crane.enable_pin(), crane.count)
        
    sleep_ms(2_000)
    
if __name__ == "__main__":
    test()

# if __name__ == "__main__":
#    test()

# END