# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from digi.xbee.devices import XBeeDevice

# TODO: Replace with the serial port where your local module is connected to.

from digi.xbee.models.address import XBee64BitAddress

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice

# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyUSB0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 230400

DATA_TO_SEND = "Hello XBee!"
REMOTE_NODE_ID = "XBEE_B"


def main():
    print(" +-----------------------------------------------------+")
    print(" | XBee Python Library Send Data Asynchronously Sample |")
    print(" +-----------------------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        # Obtain the remote XBee device from the XBee network.
        remote_device = RemoteXBeeDevice(device, 
                x64bit_addr=XBee64BitAddress(bytearray.fromhex('0013A20041AE8955')))
        print(remote_device.get_64bit_addr())
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        print("Sending data asynchronously to %s >> %s..." % (remote_device.get_64bit_addr(), DATA_TO_SEND))

        device.send_data_async(remote_device, DATA_TO_SEND)

        print("Success")

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()