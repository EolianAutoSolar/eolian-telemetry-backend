from abstract_handler import AbstractCanHandler
from abc import ABC, abstractmethod
import asyncio
import can

# BMS handler class
# It implements the converter for the BMS but with a singleton pattern so you can only instance one BMSHandler.
class BMSHandler(AbstractCanHandler):
    __id: int = 2
    __bms_id: int = 100

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance._id = cls.__id
            cls._instance._bms_id = (cls.__bms_id & 0b11111111111)
            cls._instance._external_can_bus = can.Bus(interface="socketcan", channel="can1", can_filters=[
                {"can_id": cls.__bms_id, "can_mask": 0x7F0}
            ])
            cls._instance._internal_can_bus = can.Bus(interface="socketcan", channel="can_bridge")

        return cls._instance

    def _change_id(self, message: can.Message, **params) -> can.Message:
        message.arbitration_id = (message.arbitration_id << 3) | (self._get_id() & 0b111)
        return message

    def _get_message(self) -> can.Message:
        return self._get_external_bus().recv()

    def _send_message(self, message: can.Message) -> None:
        self._get_internal_bus().send(message)

    def _run(self) -> None:
        while True:
            message: can.Message = self._get_message()
            external_message: can.Message = self._change_id(message)
            self._send_message(message)
