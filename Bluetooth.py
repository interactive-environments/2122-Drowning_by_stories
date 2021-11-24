# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import _bleio
import busio
import board
import microcontroller
import digitalio

"""
This example scans for any BLE advertisements and prints one advertisement and one scan response
from every device found.
"""

from adafruit_ble import BLERadio

u = busio.UART(tx = board.D0, rx = board.D1, baudrate = 115200)
r = digitalio.DigitalInOut(board.D12)
c = digitalio.DigitalInOut(board.D9)
adapter = _bleio.Adapter(uart = u, rts = r, cts = c)
ble = BLERadio(adapter)
print("scanning")# found = set()
scan_responses = set()
for advertisement in ble.start_scan():
    addr = advertisement.address
    if advertisement.scan_response and addr not in scan_responses:
        scan_responses.add(addr)
    elif not advertisement.scan_response and addr not in found:
        found.add(addr)
    else:
        continue
    print(addr, advertisement)
    print("\t" + repr(advertisement))
    print()

sprint("scan done")
