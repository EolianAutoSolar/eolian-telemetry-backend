from abstract_handler import AbstractCanHandler
from abc import ABC, abstractmethod
import asyncio
import can

# Abstract class for the kelly handler
# This abstract class uses a singleton pattern, so for each child class you can only instance one object.
class _AbstractKellyHandler(AbstractCanHandler):
    __id: int
    __kelly_id_query: int
    __kelly_id_response: int
    __kelly_messages: list = [0x1b, 0x1a, 0x33, 0x37, 0x42, 0x43, 0x44]

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance._id = cls.__id
            cls._instance._kelly_id_query = (cls.__kelly_id_query & 0b11111111111)
            cls._instance._kelly_id_response = cls.__kelly_id_response
            cls._instance._external_can_bus = can.Bus(interface="socketcan", channel="can0", can_filters=[
                {"can_id": cls.__kelly_id_response, "can_mask": 0xFFF}
            ])
            cls._instance._internal_can_bus = can.Bus(interface="socketcan", channel="can_bridge")
            cls._instance._kelly_messages = cls.__kelly_messages

        return cls._instance

    def _change_id(self, message: can.Message, **params) -> can.Message:
        message.arbitration_id = (params["query"] << 3) | (self._get_id() & 0b111)
        return message

    def _get_message(self, query: int) -> can.Message:
        msgQuery = can.Message(arbitration_id = self.__kelly_id_query, is_extended_id=False, data = [query])
        self._get_external_bus().send(msgQuery)

        responseMessage = self._get_external_bus().recv(timeout=0.5)
        while (responseMessage == None):
            self._get_external_bus().send(msgQuery)
            responseMessage = self._get_external_bus().recv(timeout=0.5)

        return responseMessage

    def _send_message(self, message: can.Message) -> None:
        self._get_internal_bus().send(message)

    def _run(self) -> None:
        while True:
            for query in self._kelly_messages:
                message: can.Message = self._get_message(query)
                externalMessage: can.Message = self._change_id(message, query=query)
                self._send_message(message)

# Creating a concrete Kelly handler for the left kelly and its configurations
class LeftKellyHandler(_AbstractKellyHandler):
    _AbstractKellyHandler__id: int = 0
    _AbstractKellyHandler__kelly_id_query: int = 100
    _AbstractKellyHandler__kelly_id_response: int = 105

# Creating a concrete Kelly handler for the right kelly and its configurations
class RightKellyHandler(_AbstractKellyHandler):
    _AbstractKellyHandler__id: int = 1
    _AbstractKellyHandler__kelly_id_query: int = 200
    _AbstractKellyHandler__kelly_id_response: int = 205
