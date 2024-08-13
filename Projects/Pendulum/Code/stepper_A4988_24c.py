""" stepper_A4988 - driver for boards based on the Allegro A4988 chip.

    Extensively modified by
    ProfHuster@GMail.com
    2024-07-20
    - 24b direct pin values, made code more consise.
    - 24c added position, x, get_x, set_x, to_x, mode, steps_per_mm
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
        
        self._X = 0.0
        self._MODE = 4 # 1=full, 2, 4, 8, 16 are allowed
        self._MODES = (1, 2, 4, 8, 16)
        self._STEPS_PER_MM = self._MODE * 1000.0 / 200.0

    @property 
    def x(self):
        return self._X
    
    @x.setter
    def x(self, value):
        self._X = value

    def to_x(self, x1=0.0):
        steps = round((x1 - self.x) * self._STEPS_PER_MM)
        # Because of rounding update x
        self.x += steps / self._STEPS_PER_MM
        if steps:
            self.do_steps(steps)
        return self.x

    @property
    def mode(self):
        return self._MODE
    
    @mode.setter
    def mode(self, value):
        if value in self._MODES:
            self._MODE = value
            self._STEPS_PER_MM = self._MODE * 1000.0 / 200.0
    
    @property
    def steps_per_mm(self):
        return self._STEPS_PER_MM

    def do_steps(self, n=0):
        # print("n= ", n)
        if n >= 0:
            # print("Dir 1")
            self.dir_pin(1)
            dn = 1
        else:
            # print("Dir 0")
            self.dir_pin(0)
            dn = -1
        for _ in range(abs(n)):       
            self.step_pin(1)
            sleep_ms(self.PULSE_SLEEP_MS)
            self.step_pin(0)
            sleep_ms(self.PULSE_SLEEP_MS)
            self.count += dn
            self.x += dn / self._STEPS_PER_MM
        
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
        self.PULSE_SLEEP_MS = round(50 / self.PULSE_RATE)        

def test():      
    dir_pin = 13
    step_pin = 14
    enable_pin = 15
    crane = Stepper(rate=500)
    crane.enable()
    print("Rate = ", crane.PULSE_RATE, "N_STEPS = ", N_STEPS)
    
    for _ in range(2):
        crane.do_steps(N_STEPS)
        sleep_ms(2_000)
        crane.do_steps(-N_STEPS)
            
        sleep_ms(2_000)

    crane.to_x(0)
    for _ in range(2):
        crane.to_x(10.0)
        sleep_ms(2_000)
        crane.to_x(0)
        crane.to_x(-10.0)
        sleep_ms(2_000)
    
    print(f"mode = {crane.mode}")
    print(f"steps_per_mm = {crane.steps_per_mm}")
    print("Done")
    
if __name__ == "__main__":
    test()

# if __name__ == "__main__":
#    test()

# END