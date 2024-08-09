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
from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM3"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 230400

def p(packet):
    print(packet)

def main():
    print(" +-------------------------------------------------+")
    print(" | XBee Python Library Receive Data Polling Sample |")
    print(" +-------------------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        device.flush_queues()

        # device.add_packet_received_callback(p)

        print("Waiting for data...\n")

        while True:
            remote = RemoteXBeeDevice(device, 
                    x64bit_addr=XBee64BitAddress(bytearray.fromhex('13A20041AE890D')))
            remote.set_sync_ops_timeout(0)
            xbee_message = device.read_data_from(remote)
            if xbee_message is not None:
                print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                         xbee_message.data), flush=True)

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()