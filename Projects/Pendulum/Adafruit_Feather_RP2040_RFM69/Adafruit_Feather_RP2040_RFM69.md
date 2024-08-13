# Adafruit Feather RFM69 
These are microcontrollers with built-in radio packet communication. 
It is a much simpler than LoRa. I will refer to them as `RFM69`.

They also include a LiPo battery plug and charger, and a STEMMA-QT connector.

# Start-Up
This test runs CircuitPython (CPy) on the RFM69.
- Download the latest CircuitPython `uf2` file from [here](https://circuitpython.org/board/adafruit_feather_rp2040_rfm69/). At the time of  this writing it was file `adafruit-circuitpython-adafruit_feather_rp2040_rfm-en_US-9.0.5.uf2`
- Hold down the `Boot` button (the one farthest from the USB connector), and plug into computer.
- A USB drive named `RPI-PR2` will mount.
- Drag and drop the `uf2` file on to the drive. It will copy and then the RFM69 will reboot and after it is done copying, it will disconnect and reconnect as USB drive `CIRCUITPY`.

# Test Sending and Receiving
To do the send/recv test you need two RFM69's. Load CPy on both. 

## Receiver
- Go to the AdaFruit page on the RFM [here](https://learn.adafruit.com/feather-rp2040-rfm69/rfm69-radio-demo), scroll down to `Receiver Code`, click the blue `	Download Project Bundle`. It will download `Receive_Demo.zip`. Unzip it. It will create a folder `Adafruit_Feather_RP2040_RFM69`
- Change to folder `Adafruit_Feather_RP2040_RFM69/Send_and_Receive_Demo/Receive_Demo/CircuitPython 9.x/`.
- Copy file `code.py` and the folder `lib` to the `CIRCUITPY` USB drive

Download the latest CircuitPython Bundle. When this was written, it was name `adafruit-circuitpython-bundle-9.x-mpy-20240612.zip`. Extract. 