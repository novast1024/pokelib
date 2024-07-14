from __future__ import annotations
from typing import Self, Final, SupportsIndex, Iterable
from dataclasses import dataclass, replace
import math

@dataclass(frozen = True)
class Buttons:
    state: int = 0

    names = ("Y","B","A","X","L","R","ZL","ZR","Minus","Plus","LS","RS","Home","Capture") 
  
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
    
    @classmethod
    def from_bytes(cls, b: bytes) -> Self:
        return Buttons(int.from_bytes(b, "little"))
    
    def to_bytes(self, length: SupportsIndex = 2) -> bytes:
        return self.state.to_bytes(length, "little")
    
    def to_names(self) -> list[str]:
        if self.state == 0:
            return []
        else:
            return [Buttons.names[i] for i in range(len(Buttons.names)) if self.state & (1 << i)]

@dataclass(frozen = True)
class HatSwitch(Buttons):
    names = ("Up","Right","Down","Left")

    # name      Up   Up+Right Right Down+Right Down  Down+Left Left   Up+Left Center
    # index     0       1       2       3       4       5       6       7       8
    states = (0b0001, 0b0011, 0b0010, 0b0110, 0b0100, 0b1100, 0b1000, 0b1001, 0b0000)

    @classmethod
    def from_bytes(cls, b: bytes) -> Self:
        state = int.from_bytes(b)
        return HatSwitch(HatSwitch.states[state if state < 8 else 8])

    def to_bytes(self) -> bytes:
        state = self.state
        if state & 0b0101 == 0b0101: state &= 0b1010
        if state & 0b1010 == 0b1010: state &= 0b0101
        return HatSwitch.states.index(state).to_bytes()

    def to_names(self) -> list[str]:
        if self.state == 0:
            return []
        else:
            return [HatSwitch.names[i] for i in range(len(HatSwitch.names)) if self.state & (1 << i)]

@dataclass(frozen = True)
class Joystick:
    x: float = 0.0
    y: float = 0.0

    names = ("Up","Right","Down","Left")

    def __add__(self, other: Self) -> Self:
        if self.x == 0.0 and self.y == 0.0:
            return other
        elif other.x == 0.0 and other.y == 0.0:
            return self
        else:
            return Joystick(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other: Self) -> Self:
        if other.x == 0.0 and other.y == 0.0:
            return self
        else:
            return Joystick(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> Self:
        if (self.x == 0.0 and self.y == 0.0) or other == 1.0:
            return self
        else:
            return Joystick(self.x * other, self.y * other)

    def __rmul__(self, other: float) -> Self:
        return self * other
    
    @classmethod
    def from_rad(cls, x: float):
        return Joystick(math.cos(x), -math.sin(x))
    
    @classmethod
    def from_deg(cls, x: float):
        return Joystick.from_rad(math.radians(x))
    
    @classmethod
    def from_bytes(cls, b: bytes) -> Self:
        # (0x00, 0xff) => (-1.0, 1.0)
        transform = lambda x: (x - 0x80) / 127.0 if x >= 0x80 else (x - 0x80) / 128.0
        return Joystick(transform(b[0]), transform(b[1]))

    def to_bytes(self) -> bytes:
        # (-1.0, 1.0) => (0x00, 0xff)
        transform = lambda x: int(x * 127.0 + 128.0) if x >= 0.0 else int(x * 128.0 + 128.0)
        d = math.sqrt(self.x * self.x + self.y * self.y)
        if d <= 1.0:
            return bytes(map(transform, (self.x, self.y)))
        else:
            return bytes(map(transform, (self.x / d, self.y / d)))
    
    def to_names(self, prefix: str = "") -> list[str]:
        l = []

        if self.y < 0.0:
            if self.y == -1.0:
                l.append(prefix + Joystick.names[0])
            else:
                l.append(f"{round(-self.y, 3)}*{prefix}{Joystick.names[0]}")
        elif self.y > 0.0:
            if self.y == 1.0:
                l.append(prefix + Joystick.names[2])
            else:
                l.append(f"{round(self.y, 3)}*{prefix}{Joystick.names[2]}")

        if self.x > 0.0:
            if self.x == 1.0:
                l.append(prefix + Joystick.names[1])
            else:
                l.append(f"{round(self.x, 3)}*{prefix}{Joystick.names[1]}")
        elif self.x < 0.0:
            if self.x == -1.0:
                l.append(prefix + Joystick.names[3])
            else:
                l.append(f"{round(-self.x, 3)}*{prefix}{Joystick.names[3]}")
        return l

# cached data
_DEFAULT_BUTTONS: Final[Buttons] = Buttons()
_DEFAULT_HATSWITCH: Final[HatSwitch] = HatSwitch()
_DEFAULT_JOYSTICK: Final[Joystick] = Joystick()

@dataclass(frozen = True)
class GamepadInput:
    seconds: float
    buttons: Buttons = _DEFAULT_BUTTONS
    hatswitch: HatSwitch = _DEFAULT_HATSWITCH
    leftstick: Joystick = _DEFAULT_JOYSTICK
    rightstick: Joystick = _DEFAULT_JOYSTICK

    def __add__(self, other: Self) -> Self:
        return GamepadInput(
            self.seconds,
            self.buttons + other.buttons, 
            self.hatswitch + other.hatswitch,
            self.leftstick + other.leftstick,
            self.rightstick + other.rightstick
        )
    
    def __sub__(self, other: Self) -> Self:
        return GamepadInput(
            self.seconds,
            self.buttons - other.buttons, 
            self.hatswitch - other.hatswitch,
            self.leftstick - other.leftstick,
            self.rightstick - other.rightstick
        )
    
    def __mul__(self, other: float) -> Self:
        if other == 1.0:
            return self
        else:
            return replace(self, leftstick = self.leftstick * other, rightstick = self.rightstick * other)
    
    def __rmul__(self, other: float) -> Self:
        return self * other
    
    @classmethod
    def from_bytes(cls, b: bytes, seconds: float = 0.0) -> Self:
        return GamepadInput(
            seconds,
            Buttons.from_bytes(b[0:2]),
            HatSwitch.from_bytes(b[2:3]),
            Joystick.from_bytes(b[3:5]),
            Joystick.from_bytes(b[5:7])
        )
    
    def __str__(self) -> str:
        l = self.buttons.to_names() + self.hatswitch.to_names() + self.leftstick.to_names("ls.") + self.rightstick.to_names("rs.")
        if l:
            return " + ".join(map(lambda x: f"{x}({round(self.seconds, 3)})", l))
        else:
            return str(round(self.seconds, 3))
    
    def to_bytes(self) -> bytes:
        self.buttons.to_bytes() + self.hatswitch.to_bytes() + self.leftstick.to_bytes() + self.rightstick.to_bytes()

    def to_pokecon_str(self, is_leftstick_changed = True, is_rightstick_changed = True) -> str:
        l: list = []

        btn = self.buttons.state << 2
        if is_leftstick_changed: btn |= 0x02
        if is_rightstick_changed: btn |= 0x01
        l.append(hex(btn))
        l.append(self.hatswitch.to_bytes().hex())
        if is_leftstick_changed: l.append(self.leftstick.to_bytes().hex(" "))
        if is_rightstick_changed: l.append(self.rightstick.to_bytes().hex(" "))
        return " ".join(l)
