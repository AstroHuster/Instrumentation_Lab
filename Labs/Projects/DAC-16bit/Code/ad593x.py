"""ad593x_24a - Driver for 16-bit AD5932 DAC.

ProfHuster@GMail.com
2024-06-26

I started with library for the 12-bit MCP4725 I2C bus DAC and modified it 
using the data sheet. There are several important difference.

"""

from machine import I2C

BUS_ADDRESS = 0x4C

WRITE_DATA = 0x10
WRITE_CTRL = 0x40
RESET_CMD = 0x80

#The device supports a few power down modes on startup and during operation 
POWER_DOWN_MODE = {'Off':0, '1k':1, '100k':2, 'TriS':3}
        
class AD593x:
    """Class AD593x - Driver for the AD593x DAC's."""
    
    def __init__(self,i2c, address=BUS_ADDRESS) :
        """__init__ - dac = AD593x(i2c, address=0x4C)."""
        self.i2c=i2c
        self.address=address
        self._writeBuffer=bytearray(3)
        
    def write(self,value):
        """write - Usage: dac.write()."""
        value=value & 0xFFFF
        self._writeBuffer[0]= WRITE_DATA & 0xFF
        self._writeBuffer[1]=(value>>8) & 0xFF
        self._writeBuffer[2]=value & 0xFF
        return self.i2c.writeto(self.address,self._writeBuffer)==3

    def config(self,power_down='Off',gain=0,ref=1):
        gain &= 0x1
        ref &= 0x1
        # Set up write buffer
        self._writeBuffer[0] = WRITE_CTRL
        self._writeBuffer[1] = 0
        self._writeBuffer[2] = 0
        
        # power down
        self._writeBuffer[1] |= POWER_DOWN_MODE[power_down] << 5
        
        # gain
        self._writeBuffer[2] |=  gain << 3

        # reference
        self._writeBuffer[1] |= ref
        
        return self.i2c.writeto(self.address,self._writeBuffer)==3
    
    def reset(self):
        self._writeBuffer[0] = WRITE_CTRL
        self._writeBuffer[1] = RESET_CMD>>4
        self._writeBuffer[2] = RESET_CMD & 0xFF
        return self.i2c.writeto(self.address,self._writeBuffer)==3

if __name__ == "__main__":
    print("Testing")
    from time import sleep
    from machine import Pin, I2C, ADC
    adc = ADC(Pin(26))
    sda = Pin(16, Pin.IN)
    scl = Pin(17, Pin.IN)
    i2c=machine.I2C(0,sda=sda, scl=scl, freq=100_000)
    dac = AD593x(i2c, BUS_ADDRESS)
    dac.reset()
    dac.config()
    for i in range(10):
        for i in range(0, 0xffff, 0xfff):
            dac.write(i)
            sleep(0.5)
            print(adc.read_u16())
        print()
    print("D O N E")

