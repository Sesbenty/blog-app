import logging
from typing import Callable, Union
from domain import events, commands

Message = Union[commands.Command, events.Event]
logger = logging.getLogger(__name__)


class MessageBus:
    def __init__(self):
        self._command_handlers: dict[type[commands.Command], Callable]
        self._event_handlers: dict[type[events.Event], list[Callable]]

    def handle(self, message: Message):
        if isinstance(message, events.Event):
            self.handle_event(message)
        elif isinstance(message, commands.Command):
            self.handle_command(message)
        else:
            raise Exception(f"{message} was not an Event or Command")

    def handle_event(self, event: events.Event):
        for handler in self._event_handlers[type(event)]:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                handler(event)
            except Exception:
                logger.exception("Exception handling event %s", event)
                continue

    def handle_command(self, command: commands.Command):
        try:
            handler = self._command_handlers[type(command)]
            handler(command)
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise

    def command_handler(self, command: type[commands.Command]):
        def wrapper(func):
            if command in self._command_handlers:
                raise Exception(f"the command: {command.__name__} is already registered")

            self._command_handlers[command] = func

        return wrapper

    def event_handler(self, event: type[events.Event]):
        def wrapper(func):
            if event not in self._event_handlers:
                self._event_handlers[event] = []

            self._event_handlers[event].append(func)

        return wrapper
