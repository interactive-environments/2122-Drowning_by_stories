import time
import p9813
import board

from adafruit_ble import BLERadio

ble = BLERadio()

# setup chainable LEDs
led1C = board.A0
led1D = board.A1
numLeds1 = 1
chain1 = p9813.P9813(led1C, led1D, numLeds1)

# Listening
while True:
    closest = None
    closest_rssi = -80
    closest_last_time = 0
    print("Scanning for storysets")

    # Check if the curren broadcaster is still the closest
    for entry in ble.start_scan(int, minimum_rssi=-100, timeout=1):
        now = time.monotonic()
        new = False
        if entry.address == closest:
            pass
        elif entry.rssi > closest_rssi or now - closest_last_time > 0.4:
            closest = entry.address
        else:
            continue
        closest_rssi = entry.rssi
        closest_last_time = now

        # Set LED to the colour of the current broadcaster
        if entry == 1:
            chain1[0] = (255, 0, 0)
            chain1.write()
        if entry == 2:
            chain1[0] = (0, 255, 0)
            chain1.write()
        if entry == 3:
            chain1[0] = (0, 0, 255)
            chain1.write()

        # Clear the LED if we haven't heard from anything recently.
        now = time.monotonic()
        if now - closest_last_time > 1:
            chain1[0] = (0, 0, 0)
            chain1.write()
    ble.stop_scan()
