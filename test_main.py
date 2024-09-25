from can_reader import CanReader
from frontend import ConsoleVisualization
from remote import RemoteSender
from telemetry import Telemetry

# 
sender = RemoteSender("/dev/ttyUSB0")

#
canbus = CanReader(channel='vcan0')

Telemetry([sender], [canbus]).run()