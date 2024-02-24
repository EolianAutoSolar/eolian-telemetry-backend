from abc import ABC, abstractmethod
import asyncio
import can

# Handler interface
# it have all the base methods needed for the implementations of a new can handler.
# consider that the getter methdos are related to a attribute needed to the functionality of the class.
class _ICanHandler(ABC):

    @abstractmethod
    def _get_internal_bus(self) -> can.Bus:
        '''This method gets the internal virutal can bus'''

    @abstractmethod
    def _get_external_bus(self) -> can.Bus:
        '''This method gets the external physical can bus'''

    @abstractmethod
    def _get_id(self) -> int:
        '''This method gets the internal id of the component'''

    @abstractmethod
    def _change_id(self, message: can.Message, **params) -> can.Message:
        '''This method change the id of a message to a custom one'''

    @abstractmethod
    def _get_message(self) -> can.Message:
        '''This method gets the message form the external can bus'''

    @abstractmethod
    def _send_message(self, message: can.Message) -> None:
        '''This method send a message to the internal bus'''

    @abstractmethod
    def _run(self) -> None:
        '''This method run a loop of message system'''

    @abstractmethod
    async def run_daemon(self) -> None:
        '''This method thakes the run method and it executed this one on a loop executor of asyncio'''

# Abstract class for can handlers
# This have some of the basic implementations that are repeated for all the can handlers 
# here you can see that there are some variables needed on the construction of a handler.
class AbstractCanHandler(_ICanHandler):

    def _get_internal_bus(self) -> can.Bus:
        return self._internal_can_bus

    def _get_external_bus(self) -> can.Bus:
        return self._external_can_bus

    def _get_id(self) -> int:
        return self._id

    async def run_daemon(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run)
