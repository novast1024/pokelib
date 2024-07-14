from typing import Final

from .input import GamepadInput, HatSwitch
from . import settings

# cached data
_UP: Final[HatSwitch] = HatSwitch(0b0001)
_RIGHT: Final[HatSwitch] = HatSwitch(0b0010)
_DOWN: Final[HatSwitch] = HatSwitch(0b0100)
_LEFT: Final[HatSwitch] = HatSwitch(0b1000)

def Up(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, hatswitch = _UP)

def Right(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, hatswitch = _RIGHT)

def Down(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, hatswitch = _DOWN)

def Left(seconds: float = 0.0) -> GamepadInput: 
    return GamepadInput(seconds or settings.input_seconds, hatswitch = _LEFT)

# ==================== compass direction ==============================

# cached data
_N: Final[HatSwitch] = _UP
_NE: Final[HatSwitch] = _UP + _RIGHT
_E: Final[HatSwitch] = _RIGHT
_SE: Final[HatSwitch] = _DOWN + _RIGHT
_S: Final[HatSwitch] = _DOWN
_SW: Final[HatSwitch] = _DOWN + _LEFT
_W: Final[HatSwitch] = _LEFT
_NW: Final[HatSwitch] = _UP + _LEFT

def N(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, hatswitch = _N)

def NE(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, hatswitch = _NE)

def E(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, hatswitch = _E)

def SE(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, hatswitch = _SE)

def S(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, hatswitch = _S)

def SW(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, hatswitch = _SW)

def W(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, hatswitch = _W)

def NW(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, hatswitch = _NW)
