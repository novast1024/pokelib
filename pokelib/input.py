from typing import Self, SupportsIndex
from dataclasses import dataclass, replace
import itertools
import math
from . import settings

@dataclass
class Buttons:
    state: int = 0

    def __add__(self, other: Self) -> Self:
        if self == other:
            return self
        elif self.state == 0:
            return other
        elif other.state == 0:
            return self
        else:
            return replace(self, state = self.state | other.state)

    def __sub__(self, other: Self) -> Self:
        if other.state == 0:
            return self
        else:
            return replace(self, state = (self.state | other.state) ^ other.state)

    def to_list(self, names: tuple[str] = ("Y","B","A","X","L","R","ZL","ZR","MINUS","PLUS","LS","RS","HOME","CAPTURE")) -> list[str]:
        return [names[i] for i in range(len(names)) if self.state & (1 << i)] if self.state else []

    @classmethod
    def from_bytes(cls, b: bytes) -> Self:
        return cls(int.from_bytes(b, "little"))

    def to_bytes(self, length: SupportsIndex = 2) -> bytes:
        return self.state.to_bytes(length, "little")

@dataclass
class HatSwitch(Buttons):
    def to_list(self, names: tuple[str] = ("UP","DOWN","LEFT","RIGHT")) -> list[str]:
        return super().to_list(names)

    # name      UP   UP+RIGHT RIGHT DOWN+RIGHT DOWN DOWN+LEFT  LEFT  UP+LEFT
    # index     0       1       2       3       4       5       6       7
    states = (0b0001, 0b1001, 0b1000, 0b1010, 0b0010, 0b0110, 0b0100, 0b0101, 0b0000)

    @classmethod
    def from_bytes(cls, b: bytes) -> Self:
        i = int.from_bytes(b)
        return cls(cls.states[i if i < 8 else 8])

    def to_bytes(self) -> bytes:
        state = self.state
        if state & 0b1100 == 0b1100: state &= 0b0011
        if state & 0b0011 == 0b0011: state &= 0b1100
        return HatSwitch.states.index(state).to_bytes()

@dataclass
class AnalogStick:
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
        if other == 1.0:
            return self
        else:
            return replace(self, x = other * self.x, y = other * self.y)

    def __rmul__(self, other: float) -> Self:
        return self * other

    def rotate(self, deg: float) -> Self:
        rad = math.radians(deg)
        cos = math.cos(rad)
        sin = math.sin(rad)
        return replace(self, x = self.x * cos - self.y * sin, y = self.x * sin + self.y * cos)

    def to_list(self, names: tuple[str] = ("UP","DOWN","LEFT","RIGHT")) -> list[str]:
        x = round(self.x, 2)
        y = round(self.y, 2)
        ret = []
        if y < 0.0:
            ret.append(names[0] if y == -1.0 else f"{-y}*{names[0]}")
        elif y > 0.0:
            ret.append(names[1] if y == 1.0 else f"{y}*{names[1]}")
        if x < 0.0:
            ret.append(names[2] if x == -1.0 else f"{-x}*{names[2]}")
        elif x > 0.0:
            ret.append(names[3] if x == 1.0 else f"{x}*{names[3]}")
        return ret

    @classmethod
    def from_bytes(cls, b: bytes, transform = lambda it: (it - 0x80) / 127.0 if it >= 0x80 else (it - 0x80) / 128.0) -> Self:
        return cls(transform(b[0]), transform(b[1]))

    def to_bytes(self, transform = lambda it: round(it * 127.0 + 128.0) if it >= 0.0 else round(it * 128.0 + 128.0)) -> bytes:
        abs_x = abs(self.x)
        abs_y = abs(self.y)
        if abs_x > 1.0 or abs_y > 1.0:
            if abs_x >= abs_y:
                return bytes(map(transform, (self.x / abs_x, self.y / abs_x)))
            else:
                return bytes(map(transform, (self.x / abs_y, self.y / abs_y)))
        else:
            return bytes(map(transform, (self.x, self.y)))

# ============================================================================================================================ #

class Input:
    def __init__(
            self,
            buttons: Buttons = Buttons(),
            hatswitch: HatSwitch = HatSwitch(),
            leftstick: AnalogStick = AnalogStick(),
            rightstick: AnalogStick = AnalogStick(),
            seconds: float | None = None,
    ) -> None:
        self._buttons = buttons
        self._hatswitch = hatswitch
        self._leftstick = leftstick
        self._rightstick = rightstick
        self._seconds = seconds

    @classmethod
    def from_report(cls, report: bytes) -> Self:
        return cls(
            Buttons.from_bytes(report[0:2]),
            HatSwitch.from_bytes(report[2:3]),
            AnalogStick.from_bytes(report[3:5]),
            AnalogStick.from_bytes(report[5:7]),
        )

    @property
    def report(self) -> bytes:
        return b"".join((self._buttons.to_bytes(), self._hatswitch.to_bytes(), self._leftstick.to_bytes(), self._rightstick.to_bytes(), b"\x00"))

    @property
    def state(self) -> str:
        return "+".join(itertools.chain(
            self._buttons.to_list(),
            self._hatswitch.to_list(),
            self._leftstick.to_list(("LS.UP","LS.DOWN","LS.LEFT","LS.RIGHT")),
            self._rightstick.to_list(("RS.UP","RS.DOWN","RS.LEFT","RS.RIGHT"))
        ))

    @property
    def seconds(self) -> float:
        return self._seconds if self._seconds else settings.input_seconds

    def __str__(self) -> str:
        return f"{self.state}({self.seconds})"

    def __repr__(self) -> str:
        return str(self)

    def __call__(self, seconds: float) -> Self:
        return Input(self._buttons, self._hatswitch, self._leftstick, self._rightstick, seconds)

    def __add__(self, other: Self) -> Self:
        return Input(
            self._buttons + other._buttons,
            self._hatswitch + other._hatswitch,
            self._leftstick + other._leftstick,
            self._rightstick + other._rightstick,
            other._seconds if other._seconds else self._seconds
        )

    def __sub__(self, other: Self) -> Self:
        return Input(
            self._buttons - other._buttons,
            self._hatswitch - other._hatswitch,
            self._leftstick - other._leftstick,
            self._rightstick - other._rightstick,
            other._seconds if other._seconds else self._seconds
        )

    def __mul__(self, other: float) -> Self:
        return Input(
            self._buttons,
            self._hatswitch,
            self._leftstick * other,
            self._rightstick * other,
            self._seconds
        )

    def __rmul__(self, other: float) -> Self:
        return self * other

    def __eq__(self, other: object) -> bool:
        return type(other) is Input and \
            self._buttons == other._buttons and \
            self._hatswitch == other._hatswitch and \
            self._leftstick == other._leftstick and \
            self._rightstick == other._rightstick and \
            self.seconds == other.seconds

    def rotate(self, deg: float) -> Self:
        return Input(
            self._buttons,
            self._hatswitch,
            self._leftstick.rotate(deg),
            self._rightstick.rotate(deg),
            self._seconds
        )

class LeftStickInput(Input):
    UP = Input(leftstick=AnalogStick(0.0, -1.0))
    RIGHT = Input(leftstick=AnalogStick(1.0, 0.0))
    DOWN = Input(leftstick=AnalogStick(0.0, 1.0))
    LEFT = Input(leftstick=AnalogStick(-1.0, 0.0))

    def __init__(self) -> None:
        super().__init__(buttons = Buttons(0x0400))

    def move_to(x: float, y: float) -> Input: return Input(leftstick=AnalogStick(x, y))

class RightStickInput(Input):
    UP = Input(rightstick=AnalogStick(0.0, -1.0))
    RIGHT = Input(rightstick=AnalogStick(1.0, 0.0))
    DOWN = Input(rightstick=AnalogStick(0.0, 1.0))
    LEFT = Input(rightstick=AnalogStick(-1.0, 0.0))

    def __init__(self) -> None:
        super().__init__(buttons = Buttons(0x0800))

    def move_to(x: float, y: float) -> Input: return Input(rightstick=AnalogStick(x, y))