from typing import Final

from .input import GamepadInput, Joystick
from . import settings

# cached data
_UP: Final[Joystick] = Joystick(y = -1.0)
_DOWN: Final[Joystick] = Joystick(y = 1.0)
_LEFT: Final[Joystick] = Joystick(x = -1.0)
_RIGHT: Final[Joystick] = Joystick(x = 1.0)

def Up(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = _UP)

def Down(seconds: float = 0.0) -> GamepadInput: 
    return GamepadInput(seconds or settings.input_seconds, rightstick = _DOWN)

def Left(seconds: float = 0.0) -> GamepadInput: 
    return GamepadInput(seconds or settings.input_seconds, rightstick = _LEFT)

def Right(seconds: float = 0.0) -> GamepadInput: 
    return GamepadInput(seconds or settings.input_seconds, rightstick = _RIGHT)

# ==================== compass direction ==============================

def N(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = _UP)

def NNE(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = Joystick.from_deg(67.5))

def NE(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = Joystick.from_deg(45))

def ENE(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = Joystick.from_deg(22.5))

def E(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = _RIGHT)

def ESE(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = Joystick.from_deg(337.5))

def SE(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = Joystick.from_deg(315))

def SSE(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = Joystick.from_deg(292.5))

def S(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = _DOWN)

def SSW(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = Joystick.from_deg(247.5))

def SW(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = Joystick.from_deg(225))

def WSW(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = Joystick.from_deg(202.5))

def W(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = _LEFT)

def WNW(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = Joystick.from_deg(157.5))

def NW(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = Joystick.from_deg(135))

def NNW(seconds: float = 0.0) -> GamepadInput:
    return GamepadInput(seconds or settings.input_seconds, rightstick = Joystick.from_deg(112.5))
