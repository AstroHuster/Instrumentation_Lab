import machine
import time
import ssd1306
from random import choice

sck = machine.Pin(10)
mosi = machine.Pin(11)
dc = machine.Pin(12)
cs = machine.Pin(13)
res = machine.Pin(14)

spi = machine.SPI(1, 100_000, mosi=mosi, sck=sck)
display = ssd1306.SSD1306_SPI(128, 64, spi, dc, res, cs)

display.fill(0)
display.text("Hello, Pico W", 0, 0, 2)
display.text("Color 0", 0, 10, 0)
display.text("Color 2", 0, 20, 2)
display.text("Color 3", 0, 30, 1)
display.show()
time.sleep(5)
display.fill(0)
display.show()

while True:
    for color in [1, 0]:
        print("color ", color)
        pixels = list(range(128*64))
        while len(pixels):
            i_pix = choice(pixels)
            pixels.remove(i_pix)
            col = i_pix % 128
            row = i_pix // 128
            #print(i_pix, col, row)
            display.pixel(col, row, color)
            display.show()
            time.sleep(0)


# End Of File