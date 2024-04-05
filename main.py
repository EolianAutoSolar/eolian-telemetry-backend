from can_reader import CanReader
from telemetry import Telemetry
from telemetry_core import Consumer, Process
import time
import datetime
# 
canbus = CanReader('vcan0')

class D(Process):

    def __init__(self, v) -> None:
        super().__init__()
        self.v = v

    def use_data(self, data):
        print("{} used the data {} at {}".format(self.v, data, datetime.datetime.now()))

class E(Process):

    def __init__(self, v) -> None:
        super().__init__()
        self.v = v

    def use_data(self, data):
        print("{} used the data {} at {}".format(self.v, data, datetime.datetime.now()))

a = E('A')
b = D('B')
c = D('C')
mc = Consumer([a,b,c])

Telemetry(canbus, mc).run()