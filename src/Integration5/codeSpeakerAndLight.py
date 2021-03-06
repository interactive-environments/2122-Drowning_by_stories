import board
import time
import busio
import random
from DFPlayer import DFPlayer
import p9813
import adafruit_mpr121

# Setup touch sensor
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# Setup speaker
DFP_NEXT_PIN = board.D0 # attach to RX
DFP_BUSY_PIN = board.D1 # attach to TX

# Setup volume
PLAYER_VOL = 100
dfplayer = DFPlayer(volume=PLAYER_VOL)

# Setup chainable LED
led1C = board.A0
led1D = board.A1
numLeds1 = 1
chain = p9813.P9813(led1C, led1D, numLeds1)

flag = False;

# ---------------------------------------------End Setup--------------------------------

# Fade from yellow to orange
def fade(x, y, z):
    global flag
    for i in range(x, y, z):
        chain[0] = (255, i, 0)
        chain.write()
        time.sleep(0.01)
        if not touched():
            dfplayer.stop()
            flag = False
            dfplayer.set_volume(percent=100)
            break
        if not flag:
            playConfirmation() 
            playStory(2, 7)
            flag = True


# Fade from blue to turqoise
def idle(x, y, z):
    for i in range(x, y, z):
        chain[0] = (0, 255, i)
        chain.write()
        time.sleep(0.01)
        if touched():
            fade(140, 255, 1)
            fade(255, 140, -1)

# Returns true when the touch sensor is being touched
def touched():
    if (
        mpr121[0].value
        or mpr121[1].value
        or mpr121[2].value
        or mpr121[3].value
        or mpr121[8].value
        or mpr121[9].value
        or mpr121[10].value
        or mpr121[11].value
    ):
        return True
    return False


# Chooses a story randomly out of the given range and plays that story
# a = from
# b = to
def playStory(a, b):
    i = random.randint(a, b)
    dfplayer.play(track=i)
    print("Play story")

# Plays the confirmation sound
def playConfirmation():
    dfplayer.play(track=1)
    time.sleep(2)
    dfplayer.set_volume(percent=40)


while True:
    idle(50, 255, 1)
    idle(255, 50, -1)
