import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_mpr121
import adafruit_requests as requests
import board
import busio
import time
import neopixel
import random

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
PLAYER_VOL = 80
dfplayer = DFPlayer(volume=PLAYER_VOL)

# Setup neopixels
pixel_pin = board.A1
num_pixels = 24
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.9, auto_write=False)

# Setup global flags
currZone = None
flag = False
timePast = 0

# ---------------------------------------------End Setup--------------------------------

# Fade from yellow to orange
def fade(x, y, z):
    global flag, currZone, pixels
    for i in range(x, y, z):
        pixels.fill((255, i, 0))
        pixels.show()
        time.sleep(0.05)
        if not touched():
            dfplayer.stop()
            pixels.deinit()
            pixels = neopixel.NeoPixel(
                pixel_pin, num_pixels, brightness=0.9, auto_write=False
            )
            flag = False
            break
        if not flag:
            if currZone == "ESP02":
                playConfirmation()
                playStory(1, 3)
                flag = True
            if currZone == "ESP01":
                playConfirmation()
                playStory(4, 6)
                flag = True
            # if currZone == 'ESP03':
        #                 playConfirmation()
        #                 playStory(5, 7)
        #                 flag = True
        checkNetwork()


# Fade from blue to turqoise
def idle(x, y, z):
    global pixels
    for i in range(x, y, z):
        pixels.fill((0, 255, i))
        pixels.show()
        time.sleep(0.05)
        if touched():
            pixels.deinit()
            pixels = neopixel.NeoPixel(
                pixel_pin, num_pixels, brightness=0.1, auto_write=False
            )
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
    global timePast
    timePast = time.monotonic()
    i = random.randint(a, b)
    dfplayer.play(track=i)
    print("Play story")


# Plays the confirmation sound
def playConfirmation():
    dfplayer.set_volume(percent=100)
    dfplayer.play(track=7)
    time.sleep(2)
    dfplayer.set_volume(percent=80)


# Plays the story that corresponds to the closest network
def checkNetwork():
    global currZone, flag, timePast
    closest = None
    closest_rssi = -80

    # Check if the curren broadcaster is still the closest
    for entry in esp.scan_networks():
        if not touched():
            dfplayer.stop()
            flag = False
            return
        elif (
            str(entry["ssid"], "utf-8") == "ESP02"
            or str(entry["ssid"], "utf-8") == "ESP01"
            # or str(entry["ssid"], "utf-8") == 'ESP03'
        ):
            if str(entry["ssid"], "utf-8") == closest:
                pass
            elif entry["rssi"] > closest_rssi and (timePast - 31000) <= 0:
                closest = str(entry["ssid"], "utf-8")
                closest_rssi = entry["rssi"]

    # Play stories to the current broadcaster
    if closest == "ESP02" and closest is not currZone:
        playConfirmation()
        playStory(1, 3)
    if closest == "ESP01" and closest is not currZone:
        playConfirmation()
        playStory(4, 6)
    # if closest == 'ESP03' and closest is not currZone:
    #         playConfirmation()
    #         playStory(3)
    currZone = closest


# ---------------------------------------------End helper methods-----------------------

# Print all available wifi networks
# for ap in esp.scan_networks():
#     print("\t%s\t\tRSSI: %d" % (str(ap["ssid"], "utf-8"), ap["rssi"]))

# Listening
while True:
    idle(50, 255, 1)
    idle(255, 50, -1)
