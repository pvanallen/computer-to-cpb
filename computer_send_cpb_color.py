# Example of interaction with a BLE UART device using a UART service
# implementation.
# Author: Tony DiCola
# adapted by Philip van Allen from https://github.com/adafruit/Adafruit_Python_BluefruitLE/blob/master/examples/uart_service.py
# needs https://github.com/adafruit/Adafruit_CircuitPython_BluefruitConnect
# in a local directory called adafruit_bluefruit_connect to import that
#

# sends a color value to the Circuit Plaground Bluefruit (CPB) and
# waits for the CPB to send a (light) value back
#
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
import time
from random import seed
from random import randint

# seed random number generator
seed(1)

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
def main():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices.  Good for cleaning up and
    # starting from a fresh state.
    # print('Disconnecting any connected UART devices...')
    # UART.disconnect_devices()

    # Scan for UART devices.
    print('Searching for UART device...')
    try:
        adapter.start_scan()
        # Search for the first UART device found (will time out after 60 seconds
        # but you can specify an optional timeout_sec parameter to change it).
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    print('Connecting to device...' + device.name)
    device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                      # to change the timeout.

    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
        # Wait for service discovery to complete for the UART service.  Will
        # time out after 60 seconds (specify timeout_sec parameter to override).
        print('Discovering services...')
        UART.discover(device)

        # Once service discovery is complete create an instance of the service
        # and start interacting with it.
        uart = UART(device)

        # packets are documented here https://learn.adafruit.com/bluefruit-le-connect/controller
        # color_packet_blue = b'!C\x00I\xffS'
        # color_packet_red = b'!C\xff\x02\x08\x92'
        light_value = 0
        while True:
            # build a random color
            if light_value > 10000:
                print("BRIGHT " + str(light_value))
                color_packet = ColorPacket((255,0, 0))
            else:
                print("DIM " + str(light_value))
                color_packet = ColorPacket((randint(0, 255),randint(0, 255),255))
            uart.write(color_packet.to_bytes())
            print("Sent color packet to the device.")
            time.sleep(0.2)
            print('Waiting up to 4 seconds to receive data from the device...')
            received = uart.read(timeout_sec=4)
            if received is not None:
                # Received data, print it out.
                light_value = int(received)
            else:
                # Timeout waiting for data, None is returned.
                print('Received no data!')
    finally:
        # Make sure device is disconnected on exit.
        device.disconnect()


# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
