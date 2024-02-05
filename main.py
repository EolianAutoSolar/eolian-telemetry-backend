from can_reader import CanReader
from frontend import ConsoleVisualization
from telemetry import Telemetry

# 
tui = ConsoleVisualization()

#
canbus = CanReader(channel='vcan0')

Telemetry([tui], [canbus]).run()