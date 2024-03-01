# How to test remote telemetry

This is a basic test to see wether the XBees are transmiting the required packages at the required times. It does NOT check if the data integrity is kept or how many packages are lost.

For the test 2 computers with serial ports are required, one will act as the car's telemetry and the other will act as the remote telemetry. Make sure to first configure the following settings:

1. Install the digi-xbee library with `pip install digi-xbee`.
2. Find out what serial port is the XBee assigned to in the sender and change it accordingly in line 7 of `test_main.py`.
3. Find out what serial port is the XBee assigned to in the receiver and change it accordingly in line 9 of `test_main_remote.py`.

The expected result is to see the output "Received TIMESTAMP#ID#DATA" repeteadly. Exactly one time per message sent to the local telemetry.

To run the test:

1. Run test_main.py from the sender computer.
2. Run test_main_remote.py from the receiver computer.
3. Send can messages to the sender with `cansend 111#aa` (it could be any message since they aren't processed).