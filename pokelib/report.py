from typing import Self, SupportsBytes, override
from dataclasses import dataclass, replace
import itertools
import math

@dataclass(frozen=True)
class Buttons(SupportsBytes):
    state: int = 0

    def __add__(self, other: Self) -> Self:
        if self == other or other.state == 0:
            return self
        elif self.state == 0:
            return other
        else:
            return replace(self, state = self.state | other.state)

    def __sub__(self, other: Self) -> Self:
        if other.state == 0:
            return self
        else:
            return replace(self, state = (self.state | other.state) ^ other.state)

    @override
    def __bytes__(self) -> bytes:
        return self.state.to_bytes(2, "little")

    names = ("Y","B","A","X","L","R","ZL","ZR","MINUS","PLUS","LS","RS","HOME","CAPTURE")

    def to_names(self) -> tuple[str, ...]:
        return tuple(name for i, name in enumerate(self.names) if self.state & (1 << i)) if self.state else ()

    @classmethod
    def from_name(cls, name: str) -> Self:
        return cls(1 << cls.names.index(name))

    @classmethod
    def from_bytes(cls, bytes: bytes | list[int]) -> Self:
        return cls(int.from_bytes(bytes, "little"))

class HatSwitch(Buttons):
    # name      UP   UP+RIGHT RIGHT DOWN+RIGHT DOWN DOWN+LEFT  LEFT  UP+LEFT
    # index     0       1       2       3       4       5       6       7       8
    states = (0b0001, 0b1001, 0b1000, 0b1010, 0b0010, 0b0110, 0b0100, 0b0101, 0b0000)

    @override
    def __bytes__(self) -> bytes:
        state = self.state
        if state & 0b1100 == 0b1100:
            state &= 0b0011
        if state & 0b0011 == 0b0011:
            state &= 0b1100
        return HatSwitch.states.index(state).to_bytes()

    names = ("UP","DOWN","LEFT","RIGHT")

    @classmethod
    def from_bytes(cls, bytes: bytes | list[int]) -> Self:
        i = int.from_bytes(bytes)
        return cls(cls.states[i if i < 8 else 8])

@dataclass(frozen=True)
class AnalogStick(SupportsBytes):
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: Self) -> Self:
        if self.x == 0.0 and self.y == 0.0:
            return other
        elif other.x == 0.0 and other.y == 0.0:
            return self
        else:
            return replace(self, x = self.x + other.x, y = self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        if other.x == 0.0 and other.y == 0.0:
            return self
        else:
            return replace(self, x = self.x - other.x, y = self.y - other.y)

    def __mul__(self, other: float) -> Self:
        if other == 1.0 or (self.x == 0.0 and self.y == 0.0):
            return self
        else:
            return replace(self, x = other * self.x, y = other * self.y)

    @override
    def __bytes__(self) -> bytes:
        def float2int(it: float) -> int: return round(it * 127.0 + 128.0) if it >= 0.0 else round(it * 128.0 + 128.0)
        abs_x = abs(self.x)
        abs_y = abs(self.y)
        if abs_x > 1.0 or abs_y > 1.0:
            if abs_x >= abs_y:
                return bytes((float2int(self.x / abs_x), float2int(self.y / abs_x)))
            else:
                return bytes((float2int(self.x / abs_y), float2int(self.y / abs_y)))
        else:
            return bytes((float2int(self.x), float2int(self.y)))

    def rotate(self, deg: float) -> Self:
        if deg % 360.0 == 0.0 or (self.x == 0.0 and self.y == 0.0):
            return self
        else:
            rad = math.radians(deg)
            cos = math.cos(rad)
            sin = math.sin(rad)
            return replace(self, x = self.x * cos - self.y * sin, y = self.x * sin + self.y * cos)

    names = ("UP","DOWN","LEFT","RIGHT")

    def to_names(self) -> tuple[str, ...]:
        x = round(self.x, 2)
        y = round(self.y, 2)

        return (
            (self.names[0] if y == -1.0 else f"{-y:0.2f}*{self.names[0]}",) if y < 0.0 else
            (self.names[1] if y == 1.0 else f"{y:0.2f}*{self.names[1]}",) if y > 0.0 else
            ()
        ) + (
            (self.names[2] if x == -1.0 else f"{-x:0.2f}*{self.names[2]}",) if x < 0.0 else
            (self.names[3] if x == 1.0 else f"{x:0.2f}*{self.names[3]}",) if x > 0.0 else
            ()
        )

    @classmethod
    def from_bytes(cls, bytes: bytes | list[int]) -> Self:
        def int2float(n: int) -> float: return (n - 0x80) / 127.0 if n >= 0x80 else (n - 0x80) / 128.0
        return cls(int2float(bytes[0]), int2float(bytes[1]))

    @classmethod
    def from_name(cls, name: str):
        i = cls.names.index(name)
        if i == 0:
            return cls(0.0, -1.0)
        elif i == 1:
            return cls(0.0, 1.0)
        elif i == 2:
            return cls(-1.0, 0.0)
        else:
            return cls(1.0, 0.0)

class LeftStick(AnalogStick):
    names = ("LS.UP", "LS.DOWN", "LS.LEFT", "LS.RIGHT")

class RightStick(AnalogStick):
    names = ("RS.UP", "RS.DOWN", "RS.LEFT", "RS.RIGHT")

@dataclass(frozen=True)
class Report:
    buttons: Buttons = Buttons()
    hatswitch: HatSwitch = HatSwitch()
    leftstick: LeftStick = LeftStick()
    rightstick: RightStick = RightStick()

    def __add__(self, other: Self) -> Self:
        return replace(self,
            buttons = self.buttons.__add__(other.buttons),
            hatswitch = self.hatswitch.__add__(other.hatswitch),
            leftstick = self.leftstick.__add__(other.leftstick),
            rightstick = self.rightstick.__add__(other.rightstick)
        )

    def __sub__(self, other: Self) -> Self:
        return replace(self,
            buttons = self.buttons.__sub__(other.buttons),
            hatswitch = self.hatswitch.__sub__(other.hatswitch),
            leftstick = self.leftstick.__sub__(other.leftstick),
            rightstick = self.rightstick.__sub__(other.rightstick)
        )

    def __str__(self) -> str:
        return "+".join(itertools.chain(self.buttons.to_names(), self.hatswitch.to_names(), self.leftstick.to_names(), self.rightstick.to_names()))

    def __bytes__(self) -> bytes:
        return b"".join((self.buttons.__bytes__(), self.hatswitch.__bytes__(), self.leftstick.__bytes__(), self.rightstick.__bytes__(), b"\x00"))

    @classmethod
    def from_bytes(cls, data: bytes | list[int]):
        return cls(Buttons.from_bytes(data[0:2]), HatSwitch.from_bytes(data[2:3]), LeftStick.from_bytes(data[3:5]), RightStick.from_bytes(data[5:7]))

    @classmethod
    def from_name(cls, name: str) -> Self:
        if Buttons.names.__contains__(name):
            return cls(buttons = Buttons.from_name(name))
        elif HatSwitch.names.__contains__(name):
            return cls(hatswitch = HatSwitch.from_name(name))
        elif LeftStick.names.__contains__(name):
            return cls(leftstick = LeftStick.from_name(name))
        elif RightStick.names.__contains__(name):
            return cls(rightstick = RightStick.from_name(name))
        else:
            raise ValueError()