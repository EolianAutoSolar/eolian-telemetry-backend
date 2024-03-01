from can_reader import CanReader
from frontend import ConsoleVisualization
from remote import RemoteSender
from telemetry import Telemetry

# 
sender = RemoteSender()
tui = ConsoleVisualization()

#
canbus = CanReader(channel='vcan0')
canbus2 = CanReader(channel='vcan0')

Telemetry([tui, sender], [canbus, canbus2]).run()