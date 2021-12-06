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

print("Scanning for storysets")

# Listening
while True:
    closest = None
    closest_rssi = -80
    
    # Check if the curren broadcaster is still the closest
    for entry in esp.scan_networks():
        if str(entry["ssid"], "utf-8") == 'NODE2' or str(entry["ssid"], "utf-8") == 'NODE1':
            now = time.monotonic()
            new = False
            if str(entry["ssid"], "utf-8") == closest:
                pass
            elif entry["rssi"] > closest_rssi:
                closest = str(entry["ssid"], "utf-8")
                closest_rssi = entry["rssi"]
            else:
                continue

    print(closest)
    # Set LED to the colour of the current broadcaster. Red for Iphone and blue for GNX7DE3F7
    if closest == 'NODE2':
        led[0] = (255, 0, 0)
        time.sleep(0.5)
    if closest == 'NODE1':
        led[0] = (0, 0, 255)
        time.sleep(0.5)
        

