from __future__ import annotations
from typing import Self, Final
from dataclasses import dataclass, replace
import time
from .report import Report
from . import settings

@dataclass(frozen=True)
class Input:
    report: Report = Report()
    seconds: float | None = None

    def __add__(self, other: Input) -> Self:
        return replace(self, report = self.report.__add__(other.report), seconds = self.seconds if self.seconds else other.seconds)

    def __sub__(self, other: Input) -> Self:
        return replace(self, report = self.report.__sub__(other.report), seconds = self.seconds if self.seconds else other.seconds)

    def __call__(self, seconds: float) -> Self:
        return replace(self, seconds = seconds)

    def __str__(self) -> str:
        return f"{self.report}({self.seconds or settings.input_seconds})"

    def __repr__(self) -> str:
        return self.__str__()

class Button(Input):
    pass

class HatSwitch(Input):
    pass

class LeftStick(Input):
    def __mul__(self, other: float) -> Self:
        return replace(self, report = replace(self.report, leftstick = self.report.leftstick.__mul__(other)))

    def __rmul__(self, other: float) -> Self: return self.__mul__(other)

    def rotate(self, deg: float) -> Self:
        return replace(self, report = replace(self.report, leftstick = self.report.leftstick.rotate(deg)))

class RightStick(Input):
    def __mul__(self, other: float) -> Self:
        return replace(self, report = replace(self.report, rightstick = self.report.rightstick.__mul__(other)))

    def __rmul__(self, other: float) -> Self: return self.__mul__(other)

    def rotate(self, deg: float) -> Self:
        return replace(self, report = replace(self.report, rightstick = self.report.rightstick.rotate(deg)))

class LeftStickButton(Button):
    UP: Final = LeftStick(Report.from_name("LS.UP"))
    DOWN: Final = LeftStick(Report.from_name("LS.DOWN"))
    LEFT: Final = LeftStick(Report.from_name("LS.LEFT"))
    RIGHT: Final = LeftStick(Report.from_name("LS.RIGHT"))

class RightStickButton(Button):
    UP: Final = RightStick(Report.from_name("RS.UP"))
    DOWN: Final = RightStick(Report.from_name("RS.DOWN"))
    LEFT: Final = RightStick(Report.from_name("RS.LEFT"))
    RIGHT: Final = RightStick(Report.from_name("RS.RIGHT"))

Y: Final = Button(Report.from_name("Y"))
B: Final = Button(Report.from_name("B"))
A: Final = Button(Report.from_name("A"))
X: Final = Button(Report.from_name("X"))
L: Final = Button(Report.from_name("L"))
R: Final = Button(Report.from_name("R"))
ZL: Final = Button(Report.from_name("ZL"))
ZR: Final = Button(Report.from_name("ZR"))
MINUS: Final = Button(Report.from_name("MINUS"))
PLUS: Final = Button(Report.from_name("PLUS"))
LS: Final = LeftStickButton(Report.from_name("LS"))
RS: Final = RightStickButton(Report.from_name("RS"))
HOME: Final = Button(Report.from_name("HOME"))
CAPTURE: Final = Button(Report.from_name("CAPTURE"))
UP: Final = HatSwitch(Report.from_name("UP"))
DOWN: Final = HatSwitch(Report.from_name("DOWN"))
LEFT: Final = HatSwitch(Report.from_name("LEFT"))
RIGHT: Final = HatSwitch(Report.from_name("RIGHT"))

@dataclass(frozen=True)
class Hold:
    input: Input

@dataclass(frozen=True)
class EndHold:
    input: Input | None = None

NOP: Final = Input() # no operation

@dataclass
class Combo:
    elements: list[Combo | Input]
    repeat: int

    def __init__(self, *args: Combo | Input | float | int | Hold | EndHold, repeat: int = 1) -> None:
        self.elements = self.__parse(args) if len(args) else []
        self.repeat = repeat

    def __parse(self, args: tuple[Combo | Input | float | int | Hold | EndHold, ...]) -> list[Combo | Input]:
        ret: list[Combo | Input] = []
        hold = NOP
        delay = 0.0
        auto_delay = 0.0
        for it in args:
            if isinstance(it, (float, int)):
                delay += it
            elif isinstance(it, Input):
                if it.report == NOP.report:
                    delay += it.seconds or settings.input_seconds
                else:
                    if delay or auto_delay:
                        ret.append(Input(hold.report, max(delay, auto_delay)))
                        delay = 0.0
                    ret.append(it + hold)
                    auto_delay = settings.minimum_interval
            elif isinstance(it, Combo):
                if delay or auto_delay:
                    ret.append(Input(hold.report, max(delay, auto_delay)))
                    delay = 0.0
                if it.repeat != 1:
                    ret.append(it.add_to_all_elements(hold))
                else:
                    ret += it.add_to_all_elements(hold).elements
                auto_delay = 0.0
            elif isinstance(it, Hold):
                hold += it.input
            else: # isinstance(it, EndHold)
                if delay:
                    ret.append(Input(hold.report, delay))
                    delay = 0.0
                if it.input:
                    hold -= it.input
                else:
                    hold = NOP
        if delay or auto_delay:
            ret.append(Input(hold.report, max(delay, auto_delay)))
        return ret

    def add_to_all_elements(self, input: Input) -> Combo:
        ret = Combo(repeat=self.repeat)
        ret.elements = [it + input if isinstance(it, Input) else it.add_to_all_elements(input) for it in self.elements]
        return ret

    def __add__(self, other: Combo | Input) -> Combo:
        return Combo(self, other)

    def __mul__(self, repeat: int) -> Combo:
        c = Combo(repeat = self.repeat * repeat)
        c.elements = self.elements
        return c

    def __rmul__(self, repeat: int) -> Combo: return self.__mul__(repeat)

    def __str__(self) -> str:
        return f"Combo({", ".join(map(lambda it: str(it), self.elements))}){"" if self.repeat == 1 else f"*{self.repeat}"}"

    def send(self, prev: Input = NOP) -> Input:
        for _ in range(self.repeat):
            for e in self.elements:
                if isinstance(e, Input):
                    leftstick_changed = e.report.leftstick != prev.report.leftstick
                    rightstick_changed = e.report.rightstick != prev.report.rightstick

                    btns = e.report.buttons.state
                    hat = e.report.hatswitch.__bytes__()[0]
                    lx, ly = e.report.leftstick.__bytes__()
                    rx, ry = e.report.rightstick.__bytes__()

                    btns <<= 2
                    if leftstick_changed:
                        btns |= 0x02
                    if rightstick_changed:
                        btns |= 0x01

                    cmd = b""
                    if leftstick_changed:
                        if rightstick_changed:
                            cmd = f"{btns:x} {hat:x} {lx:x} {ly:x} {rx:x} {ry:x}\r\n".encode()
                        else:
                            cmd = f"{btns:x} {hat:x} {lx:x} {ly:x}\r\n".encode()
                    else:
                        if rightstick_changed:
                            cmd = f"{btns:x} {hat:x} {rx:x} {ry:x}\r\n".encode()
                        else:
                            cmd = f"{btns:x} {hat:x}\r\n".encode()

                    if cmd[0] < ord("0") or ord("9") < cmd[0]:
                        cmd = b"0" + cmd

                    if settings.python_command:
                        if settings.input_visible:
                            print(e)
                        settings.python_command.keys.ser.ser.write(cmd)
                        time.sleep(e.seconds or settings.input_seconds)
                        if e.report == NOP.report:
                            settings.python_command.checkIfAlive()
                    elif settings.serial:
                        if settings.input_visible:
                            print(e)
                        settings.serial.write(cmd)
                        time.sleep(e.seconds or settings.input_seconds)
                    prev = e
                else:
                    prev = e.send(prev)
        return prev

def send(arg0: Combo | Input | float | int, *args: Combo | Input | float | int):
    last = Combo(arg0, *args).send()
    if last.report != NOP.report:
        Combo(NOP).send(last)