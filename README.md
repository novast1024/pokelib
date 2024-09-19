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
from pokelib import *
```
settings
```
settings.python_command = self
settings.input_seconds = 0.05
settings.minimum_interval = 0.05
settings.input_visible = False
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
from pokelib import *

class Test(ImageProcPythonCommand):
    NAME = "くるくるくる"

    def do(self):
        settings.python_command = self
        settings.input_seconds = 0.03
        settings.minimum_interval = 0.0
        settings.input_visible = True

        rotate_right = Combo()
        for deg in range(0, 360, 15):
            rotate_right += Combo(LS.UP.rotate(deg))

        send(rotate_right*3)
```
