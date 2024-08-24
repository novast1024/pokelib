from typing import Final
from .input import *

Y: Final[Input] = Input(buttons=Buttons(0x01))
B: Final[Input] = Input(buttons=Buttons(0x02))
A: Final[Input] = Input(buttons=Buttons(0x04))
X: Final[Input] = Input(buttons=Buttons(0x08))
L: Final[Input] = Input(buttons=Buttons(0x10))
R: Final[Input] = Input(buttons=Buttons(0x20))
ZL: Final[Input] = Input(buttons=Buttons(0x40))
ZR: Final[Input] = Input(buttons=Buttons(0x80))
MINUS: Final[Input] = Input(buttons=Buttons(0x0100))
PLUS: Final[Input] = Input(buttons=Buttons(0x0200))
LS: Final[LeftStickInput] = LeftStickInput()
RS: Final[RightStickInput] = RightStickInput()
HOME: Final[Input] = Input(buttons=Buttons(0x1000))
CAPTURE: Final[Input] = Input(buttons=Buttons(0x2000))

UP: Final[Input] = Input(hatswitch=HatSwitch(0x01))
DOWN: Final[Input] = Input(hatswitch=HatSwitch(0x02))
LEFT: Final[Input] = Input(hatswitch=HatSwitch(0x04))
RIGHT: Final[Input] = Input(hatswitch=HatSwitch(0x08))