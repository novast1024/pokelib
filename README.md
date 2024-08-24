# My Poke-Controller MODIFIED Library

install
```
pip install git+https://github.com/novast1024/pokelib
```
uninstall
```
pip uninstall pokelib
```
import
```
from pokelib.combo import *
from pokelib.constants import *
from pokelib import settings
```
initialize
```
settings.python_command = self
settings.input_seconds = 0.05
settings.minimum_interval = 0.05
```

constants
```
Y B A X L R ZL ZR MINUS PLUS LS RS HOME CAPTURE # Buttons
UP DOWN LEFT RIGHT # Hat Switch
LS.UP LS.DOWN LS.LEFT LS.RIGHT # Left Stick
RS.UP RS.DOWN RS.LEFT RS.RIGHT # Right Stick
```
example
```
from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand

from pokelib import settings
from pokelib.constants import *
from pokelib.combo import *

class Test(ImageProcPythonCommand):
    NAME = "テスト"

    def do(self):
        settings.python_command = self
        settings.input_seconds = 0.01
        settings.minimum_interval = 0.0

        c = Combo()
        for i in range(0, 360, 15):
            c += Combo(LS.UP.rotate(i))
        
        send(c*5)
```

```
c = Combo(
    Combo(A)*5, 4,

    Combo(DOWN)*2, Combo(RIGHT)*3, LEFT, A, 4,

    RIGHT, Combo(DOWN)*2, A, # s
    Combo(RIGHT)*5, UP, A, # u
    RIGHT, UP, A, # k
    Combo(LEFT)*7, A, # a
    Combo(RIGHT)*10, Combo(UP)*2, # -
    Combo(LEFT)*7, DOWN, A, # r
    LEFT, A, # e
    Combo(RIGHT)*2, A, # t
    A, # t
    Combo(RIGHT)*4, A, # o
    PLUS, 4,

    Combo(A)*1100,

    LS.DOWN(3), 5, LS.LEFT(6),
    X, 1, A, 1, Combo(RIGHT, 0.1, DOWN, 0.1)*4, Combo(A(1.5), 1.5)*4, B, 1, B,
    LS.UP(2), LS.LEFT(3.5), LS.DOWN(2.5),
    Combo(A)*30, LS.DOWN(3.5), LS.LEFT(7.5),
    Combo(A)*100, LS.DOWN+LS.RIGHT(1.5), LS.RIGHT(7.5),
    Combo(A)*180, LS.RIGHT(1.5), LS.UP+LS.RIGHT(2), LS.UP(4), LS.RIGHT(4.5), LS.DOWN(2.3), LS.RIGHT(2.0),
    Combo(A)*100, LS.UP+LS.LEFT(4), LS.LEFT(3.5), LS.DOWN(4.1), LS.LEFT(2),
    Combo(A)*130, LS.DOWN+LS.RIGHT(5.0), Combo(A)*420, Y, 3, Combo(A)*4, 1, X, DOWN, A,
)
```
