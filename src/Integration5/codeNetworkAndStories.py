import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_mpr121
import adafruit_requests as requests
import board
import busio
import p9813
import random
import time

from adafruit_esp32spi import adafruit_esp32spi
from DFPlayer import DFPlayer
from digitalio import DigitalInOut

# ---------------------------------------------End library imports----------------------

# Setup esp32
esp32_cs = DigitalInOut(board.D9)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

# Setup socket
requests.set_socket(socket, esp)

# Setup touch sensor
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# Setup dfplayer
PLAYER_VOL = 40
dfplayer = DFPlayer(volume=PLAYER_VOL)

# Setup chainable LED
led1C = board.A0
led1D = board.A1
numLeds1 = 1
chain = p9813.P9813(led1C, led1D, numLeds1)

# ---------------------------------------------End Setup--------------------------------

# Fade from yellow to orange
def fade(x, y, z):
    for i in range(x, y, z):
        chain[0] = (255, i, 0)
        chain.write()
        time.sleep(0.01)
        if not touched():
            dfplayer.stop()
            break
        checkNetwork()


# Fade from blue to turqoise
def idle(x, y, z):
    for i in range(x, y, z):
        chain[0] = (0, 255, i)
        chain.write()
        time.sleep(0.01)
        if touched():
            dfplayer.set_volume(percent=100)
            dfplayer.play(track=1)
            dfplayer.set_volume(percent=40)
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

# Plays the story that corresponds to the closest network
def checkNetwork():
    closest = None
    closest_rssi = -80

    # Check if the curren broadcaster is still the closest
    for entry in esp.scan_networks():
        if str(entry["ssid"], "utf-8") == closest:
            pass
        elif entry["rssi"] > closest_rssi:
            closest = str(entry["ssid"], "utf-8")
        else:
            continue
        closest_rssi = entry["rssi"]

        # Play story of the story pool of the current broadcaster
        if closest == 'iPhone':
            playStory(2, 4)
        if closest == 'GNX7DE3F7':
            playStory(5, 7)

# ---------------------------------------------End helper methods-----------------------

# Print all available wifi networks
for ap in esp.scan_networks():
    print("\t%s\t\tRSSI: %d" % (str(ap["ssid"], "utf-8"), ap["rssi"]))

# Listening
while True:
    idle(50, 255, 1)
    idle(255, 50, -1)

