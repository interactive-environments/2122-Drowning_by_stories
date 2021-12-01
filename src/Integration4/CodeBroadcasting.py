from adafruit_ble import BLERadio

ble = BLERadio()

# Broadcasting
advertisement = 3  # Change this to the right broadcaster

while True:
    print("Broadcasting number")
    ble.start_advertising(advertisement)
    ble.stop_advertising()
