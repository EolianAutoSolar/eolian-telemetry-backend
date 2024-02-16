from can_reader import CanReader
from frontend import ConsoleVisualization
from telemetry import Telemetry

# 
tui = ConsoleVisualization()

#
canbus = CanReader(channel='vcan0')
canbus2 = CanReader(channel='vcan0')

Telemetry([tui], [canbus, canbus2]).run()