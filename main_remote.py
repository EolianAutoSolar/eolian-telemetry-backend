from can_reader import CanReader
from frontend import ConsoleVisualization
from remote import RemoteReceiver
from telemetry import Telemetry

# 
tui = ConsoleVisualization()

#
recv = RemoteReceiver()

Telemetry([], [recv]).run()