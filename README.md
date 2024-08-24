# pokelib

install & uninstall
```
pip install git+https://github.com/novast1024/pokelib
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
