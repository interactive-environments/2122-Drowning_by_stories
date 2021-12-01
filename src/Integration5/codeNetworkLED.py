import board
import busio
import time
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_dotstar

# Setup internal LED
led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
led.brightness = 0.3

# Setup esp32
esp32_cs = DigitalInOut(board.D9)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)

# Initiate spi & esp32
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

# Request to set a socket with the esp value
requests.set_socket(socket, esp)

# Scan the network for all the wifi networks
for ap in esp.scan_networks():
    print("\t%s\t\tRSSI: %d" % (str(ap["ssid"], "utf-8"), ap["rssi"]))

# Listening
while True:
    closest = None
    closest_rssi = -80
    closest_last_time = 0
    # print("Scanning for storysets")

    # Check if the curren broadcaster is still the closest
    for entry in esp.scan_networks():
        print(closest)
        print(closest_rssi)
        now = time.monotonic()
        new = False
        if str(entry["ssid"], "utf-8") == closest:
            pass
        elif entry["rssi"] > closest_rssi or now - closest_last_time > 0.4:
            closest = str(entry["ssid"], "utf-8")
        else:
            continue
        closest_rssi = entry["rssi"]
        closest_last_time = now

        # Set LED to the colour of the current broadcaster. Red for Iphone and blue for GNX7DE3F7
        if closest == 'iPhone':
            led[0] = (255, 0, 0)
            time.sleep(0.5)
        if closest == 'GNX7DE3F7':
            led[0] = (0, 0, 255)
            time.sleep(0.5)

        # Clear the LED if we haven't heard from anything recently.
        now = time.monotonic()
        if now - closest_last_time > 1:
            led[0] = (0, 0, 0)
            time.sleep(0.5)
