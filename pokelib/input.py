from typing import Self, Final
from dataclasses import dataclass, replace
import math

@dataclass(frozen = True)
class ButtonInput:
    value: int = 0
        
    def __add__(self, other: Self) -> Self:
        if self == other:
            return self
        elif self.value == 0:
            return other
        elif other.value == 0:
            return self
        else:
            return replace(self, value = self.value | other.value)
    
    def __sub__(self, other: Self) -> Self:
        if other.value == 0:
            return self
        else:
            return replace(self, value = (self.value | other.value) ^ other.value)
    
    def encode(self) -> bytes:
        return self.value.to_bytes(length = 2, byteorder = "little")

@dataclass(frozen = True)
class HatSwitchInput(ButtonInput):
    def encode(self) -> bytes:
        #           up   up+right right down+right down  down+left left   up+left center
        # index     0       1       2       3       4       5       6       7       8
        values = [0b0001, 0b0011, 0b0010, 0b0110, 0b0100, 0b1100, 0b1000, 0b1001, 0b0000]
        v = self.value
        if v & 0b0101 == 0b0101: v &= 0b1010
        if v & 0b1010 == 0b1010: v &= 0b0101
        return values.index(v).to_bytes()

@dataclass(frozen = True)
class StickInput:
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: Self) -> Self:
        if self.x == 0.0 and self.y == 0.0:
            return other
        elif other.x == 0.0 and other.y == 0.0:
            return self
        else:
            return StickInput(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other: Self) -> Self:
        if other.x == 0.0 and other.y == 0.0:
            return self
        else:
            return StickInput(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> Self:
        if (self.x == 0.0 and self.y == 0.0) or other == 1.0:
            return self
        else:
            return StickInput(self.x * other, self.y * other)

    def __rmul__(self, other: float) -> Self:
        return self * other

    def encode(self) -> bytes:
        # (-1.0, 1.0) -> (0x00, 0xff)
        transform = lambda x: int(x * 127.0 + 128.0) if x >= 0.0 else int(x * 128.0 + 128.0)
        d = math.sqrt(self.x * self.x + self.y * self.y)
        if d <= 1.0:
            return bytes(map(transform, (self.x, self.y)))
        else:
            return bytes(map(transform, (self.x / d, self.y / d)))

# cached data
_DEFAULT_BUTTON_INPUT: Final[ButtonInput] = ButtonInput()
_DEFAULT_HATSWITCH_INPUT: Final[HatSwitchInput] = HatSwitchInput()
_DEFAULT_STICK_INPUT: Final[StickInput] = StickInput()

@dataclass(frozen = True)
class GamepadInput:
    seconds: float
    button: ButtonInput = _DEFAULT_BUTTON_INPUT
    hatswitch: HatSwitchInput = _DEFAULT_HATSWITCH_INPUT
    leftstick: StickInput = _DEFAULT_STICK_INPUT
    rightstick: StickInput = _DEFAULT_STICK_INPUT

    def __add__(self, other: Self) -> Self:
        return GamepadInput(
            self.seconds,
            self.button + other.button, 
            self.hatswitch + other.hatswitch,
            self.leftstick + other.leftstick,
            self.rightstick + other.rightstick
        )
    
    def __sub__(self, other: Self) -> Self:
        return GamepadInput(
            self.seconds,
            self.button - other.button, 
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
    
    def encode(self) -> bytes:
        return self.button.encode() + self.hatswitch.encode() + self.leftstick.encode() + self.rightstick.encode()
    
    def to_pokecon_str(self, is_leftstick_changed = True, is_rightstick_changed = True) -> str:
        l: list = []

        btn = self.button.value << 2
        if is_leftstick_changed: btn |= 0x02
        if is_rightstick_changed: btn |= 0x01
        l.append(hex(btn))
        l.append(self.hatswitch.encode().hex())
        if is_leftstick_changed: l.append(self.leftstick.encode().hex(" "))
        if is_rightstick_changed: l.append(self.rightstick.encode().hex(" "))
        return " ".join(l)
