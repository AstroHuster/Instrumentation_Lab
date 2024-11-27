# Adafruit MQTT

The situation very common in the world today is having many small smart sensors that can connect to the Internet. This document takes you through one way these sensors communicate to the Internet. One standard is MQTT (Message Queueing Telemetry Transport.) We will use this protocol and the https://io.adafruit.com web site to post our environmental data.

Our situation is that we have Raspberry Pi's that collect data from microcontrollers, Teensy's and TinyPICO's. We want to make this data accessible on the Internet.

One great thing about the TP's (TinyPICO's) is that have built-in WiFi, so if they are connected to a local WiFi, they can send their data out themselves without going through the RPi (Raspberry Pi.)

## MQTT

We are interested in putting the data our microcontrollers and Raspberry Pi's someplace on the Internet, so MQTT is a great protocol for doing this.

The AdaFruit web site has great lesson for learning about all kinds of technical topics including MQTT. The rest of this document is based on [Intro to Adafruit_MQTT ](https://learn.adafruit.com/mqtt-adafruit-io-and-you/intro-to-adafruit-mqtt).

<b><i>Follow along on both this web page and the directions below!</i></b>

## Account

Use the web site [IO - Adafruit](https://io.adafruit.com)

- User: profhuster

- Password: 05Einstein05!

When you work through the pages, it tell you how to find your key. It is the same for all of the profhuster dashboards and feeds, so *do not change the key*! The web site looks a little different than the examples. If you login you will be at the page https://io.adafruit.com/profhuster/dashboards In the top right of the nav bar, click **My Key**. A pop up shows the key information. It should be:

- `ca3bb52aed014c99b17b095bc2f98ed2`

- **Do not regenerate the key!** If you do all devices posting to this account will be cut off.

Next the lesson directs you to create two feeds at [Adafruit IO Basics: Feeds](https://learn.adafruit.com/adafruit-io-basics-feeds). 

## Dashboards, Groups, and Feeds

I created dashboards for each one of us, `a-boyer`, `t-aumer`, and `p-huster`. Use the dashboard I created for you.

**Create a Group**. The *Feeds* link is now in the Nav bar at the top of the *Dashboards* page instead of in a nav bar on the left of the page. On the *Feeds* page there are two nice large buttons, *+ New Group* and *+ New Feed*. Create a group for your feeds named *Your Name 2021*.

**Create two feeds**. Name them *CPU-Temperature* and *onoff*.

Once you have created the feeds, go back to the *Dashboards* page and click on your dashboard. There won't be any content on it, but you will add a display for the CPU temperature.

- Click on the gear, ⚙ => **Create New Block** => **Gauge** (the top left icon)

- Connect it to a feed. In your Groups, select *CPU-Temperature* and click *Next Step*

- Set the min and max values to 0 and 150. These are degrees celsius. 

- Fill in other information as you think appropriate.

- Click *Create Block*.

- Make another block using an ON-OFF toggle and connect it to your *onoff* feed.

- You can place them side-by-side by clicking the gear icon and selecing *Edit Layout*.

- Finally click the Gear icon and Privacy and make the dashboard public.

- Here is my result (though with the TP working!)

![](C:\Users\mhust\AppData\Roaming\marktext\images\2021-04-05-16-56-09-image.png)

The next page in the tutorial is *Arduino+Library Setup*. Instead of this, we are going to use the TinyPICO.

# Starting your TinyPICO

- Plug in your TinyPICO and connect to it with *rshell*. (**Note**: If you do not have rshell, you can skip down and install *Thonny*.)
  
  - On Windows I start the *Device Manager* => Ports. The TP is listed as *Silicon Labs CP210x USB to UART bridge*. It moves around. I am using it a *COM3* for this example.
  
  - Start a Windows Terminal or Command window.
  
  - `rshell --buffer-size 512 -p COM3`
  
  - **Note**: I have trouble seeing the files when I do `ls`, so I start it with the nocolor option.
  
  - `rshell -n --buffer-size 512 -p COM3`
  
  - `repl` to start uPy (micropython)

```
import network
sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan()                             # Scan for available access points
sta_if.connect("Ruthless", "Georgeless") # Connect to an AP
sta_if.isconnected()
```

- Test Internet connection:

- `from uping import ping`

- `ping("google.com")`   # Connected if it finds google!

# Install the Thonny IDE

- If you are working with the TinyPICO (TP) connected to your Raspberry Pi (RPi), Thonny is already on the RPi! Otherwise (or if you want to program the TP directly from your laptop) install Thonny.

- Install *Thonny* python editor-IDE. You can directly load python files to a microcontroller from *Thonny*.

- *Thonny* is an IDE (Integrated Developement Environment) for python. It comes installed on RPi, and is available on Windows, Mac, and Linux.

- Versions of Thonny after 3.1 have a very nice built in micropython capability!

- Plug your TP into the RPi or your laptop.

- Start Thonny.

- Click **View** => **Shell**. to see a python prompt `>>>`
  
  - If you did not do the above python steps above, do them now in the shell view.

- Click **Tools** => **Options** => **Interpreter**. Select **Micropython (ESP32)**. 
  
  - And **Port** => **Silicon Labs CP210x USB to UART Bridge (COM3)**.
  
  - **Note**: your port will probably be different. On Mac's and Linux, the port with be `/dev/tty<Something>`.

- Thonny should connect. 

![](C:\Users\mhust\AppData\Roaming\marktext\images\2021-04-05-07-52-58-image.png)

- The TP is running a program I wrote and saved on the TP as `main.py`.

> **Important Notes on Using the Shell from Thonny**
> 
> 1. When the TP is reset it will print some diagnostics and look dead. Type ^C to get the python `>>>` prompt.
> 
> 2. If you want to stop a program, type ^C.
> 
> 3. Sometimes when you try to save a file to the TP, a window pops up saying, "Device is busy." Don't panic. Click in the shell view and type ^C. When you try again it should be OK.
> 
> 4. Open the Files view in Thonny. There is a section showing you all of the files on the TP. `boot.py` and `main.py` are there along with other files you upload. You can run any file from the python prompt by typing `import filebase` where `filebase` is the file name without the `.py` at the end.

- I typed <^C> to stop and get the python `>>>` prompt.

- `help()` and the TP printed information.

- Whenever you open or save a file Thonny gives you the choice of 1) on your computer, or 2) on the micropython device
  
  - This a is great feature!

- Wire an LED in series with a resistor (value not critical, any value from 100 to 2200 will do) from pin 5 to GND. The TP pin locations are weird. Pin 5 is the fourth from the USB connector on the left side between pind 18 and 22. The ground pin is marked G and is the second one from the end on the right.

- Type this code in at the prompt. The LED should come on. Change the 1 to a 0 to turn it off.

```
from machine import Pin
Pin(5, Pin.OUT).value(1)
```

# Using MQTT and *io.adafruit.com*

I attached a zip file that includes all of the file you need to upload to your TP. Unzip it in the directory you make for this project. Then follow along the steps below.

## Install the *umqtt* Module

- In Thonny click **View** => **Shell**. This should open a command shell directly to MicroPython running on your device.

- In Thonny click **View** => **Files**. There should be a section labeled **MicroPython Device**, as in the figure.

<img src="file:///C:/Users/mhust/AppData/Roaming/marktext/images/2021-04-05-12-52-20-image.png" title="" alt="" width="240">

- In this example there are only the two essential files, *boot.py* and *main.py*.

- Right-click in the *MicroPython Device* section, select *New directory...* and create a directory `umqtt`.

- In Thonny, click **Open**, => **This computer** and navigate into the folder created by *git*  command to `micropython-lib/umqtt.simple/umqtt` and open `simple.py`.

- Click **File** => **Save as...** => **MicroPython device**. Navigate into `umqtt` and save the file `simple.py`. 

- When you save a file on the MicroPython device, the Thonny tab adds brackets around the file name, so your tab should be `[simple.py]`.

- Also, in the **File** view, you can click open the `umqtt` directory ans you should see `simple.py` there.

- You can test that you have these files in the right place by typing in the shell

```
>>> from umqtt.robust import MQTTClient
```

* There should not be any errors.

## Publish to *io.adafruit.com*

- I modified the python programs at [Using MQTT to Publish/Subscribe to adafruit io](https://github.com/miketeachman/micropython-adafruit-mqtt-esp8266)
  
  - [To publish](https://raw.githubusercontent.com/miketeachman/micropython-adafruit-mqtt-esp8266/master/publishAdafruit.py)
  
  - [To subscribe](https://raw.githubusercontent.com/miketeachman/micropython-adafruit-mqtt-esp8266/master/subscribeAdafruit.py)
  
  - [Both](https://raw.githubusercontent.com/miketeachman/micropython-adafruit-mqtt-esp8266/master/pubAndSub.py)

- When you unzip the zip file you should see several files I modified the above files.

- In Thonny open, **This Computer** =>  `pub_CPUTemp_Ada.py`

- Scroll down and change:
  
  -  *Ruthless* to (Your Wifi network)
  
  - *Georgeless *to (Your WiFi password)
  
  - Keep the user name*profhuster*
  
  - Keep the key as *ca3bb52aed014c99b17b095bc2f98ed2*

- Change`ADAFRUIT_IO_FEEDNAME` to your feed name for the temperature. 
  
  - To find the name of your feed, login to `io.adafruit.com`.
  
  - Go to **Feeds** => **Show all**. It should look like the figure below.

![](C:\Users\mhust\AppData\Roaming\marktext\images\2021-04-05-18-58-55-image.png)

- This figure only shows one group. After you add your feeds as directed in the beginning of this document, your group will show up and have your feeds. Click on the temperature *in your group*! The full feed name is at the end of the URL. In my case the full feed name is circled in the figure below; it is `prof-huster-2021.cpu-temperature`. Yours will have the name of your group in feed name.

![](C:\Users\mhust\AppData\Roaming\marktext\images\2021-04-05-19-05-28-image.png)

- You need to edit the python file and change the feedname.

- Click **File** => **Save as...** => **MicroPython device** => `pub_CPUTemp_Ada.py`

- - Now it is saved on the TP.
  
  - **Important Note**: I did some editing to the file on the TP. When the code was done I did *Save as...* back to my computer. Otherwise the only good copy of the code would be on the TP and I would not have a working copy of the code on my computer!

## NOTE: You have to modify the code!

The code I attached published to the `profhuster` dashboard and feeds. You have to make minor changes in the code to publish to your own groups & feeds & dashboards!

- I have attached:
  
  - `pub_CPUTemp_Ada.py`  - publishes the TP temperature.
  
  - `sub_OnOff_Ada.py` - subscribes to the On/Off Switch. You can control the LED from anywhere with Internet connectivity!
  
  - `pub_sub_Ada.py` - Does both simultaneously.

- To run these, you have to load them to your TP device. To run them, reset the TP by typing ^D, then at the python prompt type `import basename` (the file name without the `.py`)

## Restarting the TP MicroPython Device

- There are two ways to restart the TinyPICO MicroPython device, soft and hard.

- To do a soft reset, type <^D>. You should see any messages printed by boot.py and main.py. Type <^C> to get to the REPL `>>>` prompt.

- To do a hard reset, press the reset button on the device itself. This usually produces more output. Type <^C> to get to the prompt.
