from typing import Final

from .input import GamepadInput, Buttons
from . import settings

# cached data
_Y: Final[Buttons] = Buttons(0x01)
_B: Final[Buttons] = Buttons(0x02)
_A: Final[Buttons] = Buttons(0x04)
_X: Final[Buttons] = Buttons(0x08)
_L: Final[Buttons] = Buttons(0x10)
_R: Final[Buttons] = Buttons(0x20)
_ZL: Final[Buttons] = Buttons(0x40)
_ZR: Final[Buttons] = Buttons(0x80)
_MINUS: Final[Buttons] = Buttons(0x0100)
_PLUS: Final[Buttons] = Buttons(0x0200)
_LS: Final[Buttons] = Buttons(0x0400)
_RS: Final[Buttons] = Buttons(0x0800)
_HOME: Final[Buttons] = Buttons(0x1000)
_CAPTURE: Final[Buttons] = Buttons(0x2000)


def Y(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _Y)

def B(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _B)

def A(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _A)

def X(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _X)

def L(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _L)

def R(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _R)

def ZL(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _ZL)

def ZR(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _ZR)

def Minus(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _MINUS)

def Plus(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _PLUS)

def LS(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _LS)

def RS(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _RS)

def Home(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, buttons = _HOME)

def Capture(seconds: float = 0.0) -> GamepadInput: 
    return GamepadInput(seconds or settings.input_seconds, buttons = _CAPTURE)
