from typing import Protocol

class Serial(Protocol):
    def write(self, data: bytes) -> int:
        ...

class Sender(Protocol):
    @property
    def ser(self) -> Serial:
        ...

class Keys(Protocol):
    @property
    def ser(self) -> Sender:
        ...

class PythonCommand(Protocol):
    @property
    def keys(self) -> Keys:
        ...

    def checkIfAlive(self):
        ...

input_visible: bool = False
input_seconds: float = 0.05
minimum_interval: float = 0.05
python_command: PythonCommand | None = None
serial: Serial | None = None