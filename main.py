from can_reader import CanReader
from frontend import ConsoleVisualization
from telemetry import Telemetry
from telemetry_core import Consumer, Process

# 
tui = ConsoleVisualization()

class D(Process):

    def __init__(self, v) -> None:
        super().__init__()
        self.v = v

    def use_data(self, data):
        print("{} used the data".format(self.v))

a = D('A')
b = D('B')
c = D('C')

Telemetry([tui], [canbus, canbus2]).run()