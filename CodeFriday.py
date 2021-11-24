import time
import board
import busio
import p9813
import adafruit_mpr121
from digitalio import DigitalInOut, Direction
from DFPlayer import DFPlayer

# Setup buttons
button1 = DigitalInOut(board.D2)
button1.direction = Direction.INPUT

# Setup touch sensor
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# Setup chainable LED
led1C = board.A0
led1D = board.A1
numLeds1 = 1
chain1 = p9813.P9813(led1C, led1D, numLeds1)

# Set volume speaker
PLAYER_VOL   = 80
# PLAYER_RX  = board.RX   # board.D3
# PLAYER_TX  = board.TX   # board.D4
dfplayer = DFPlayer(volume=PLAYER_VOL)

# Fade from yellow to orange
def fade(x, y, z):
    for i in range(x, y, z):
        chain1[0] = (255, i, 0)
        chain1.write()
        time.sleep(0.01)
        if not check():
            dfplayer.stop()
            break
        ButtonPress()

# Fade from blue to turqoise
def fade1(x, y, z):
    for i in range(x, y, z):
        chain1[0] = (0, 255, i)
        chain1.write()
        time.sleep(0.01)
        if check():
            fade(140, 255, 1)
            fade(255, 140, -1)
            time.sleep(0.01)

# Checks if the touch sensor is being touched
def check():
    if mpr121[2].value or mpr121[3].value:
        return true

def ButtonPress():
    # If button1 is pressed play a story
    if button1.value:
        if dfplayer.get_status() != DFPlayer.STATUS_BUSY:
            print("switching to next story")
            dfplayer.next()

while True:
    # Start fading
    fade1(127, 255, 1)
    fade1(255, 127, -1)









