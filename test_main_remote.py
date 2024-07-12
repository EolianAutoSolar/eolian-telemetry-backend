from can_reader import CanReader
from frontend import ConsoleVisualization
from remote import RemoteReceiver
from telemetry import Telemetry

# 

#
recv = RemoteReceiver("COM1")

Telemetry([], [recv]).run()