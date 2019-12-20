# CircuitPython recieve a color via BLE
# adapted from https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/playground-color-picker
# Philip van Allen

import board
import analogio
import neopixel
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)
light = analogio.AnalogIn(board.LIGHT)

while True:
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    ble.stop_advertising()

    while ble.connected:
        packet = Packet.from_stream(uart_server)
        if isinstance(packet, ColorPacket):
            if packet.color != None
                # display packet that came in from computer
                print(packet.color)
                print(packet.to_bytes())
                # set all NeoPixels to the received color
                pixels.fill(packet.color)
                # send the current light value
                brightness = light.value
                message = str(brightness)
                uart_server.write(message)
                print(message)
