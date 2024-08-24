from typing import Self
from dataclasses import dataclass
import time

from .input import Input
from . import settings

EMPTY = Input()

def isEmpty(input: Input):
    return input._buttons == EMPTY._buttons and \
           input._hatswitch == EMPTY._hatswitch and \
           input._leftstick == EMPTY._leftstick and \
           input._rightstick == EMPTY._rightstick

@dataclass(frozen=True)
class Hold:
    input: Input

@dataclass(frozen=True)
class EndHold:
    input: Input | None = None

class Combo:
    def __init__(self, *args: Self|Input|float|int|Hold|EndHold) -> None:
        self._pool = self._parse(args) if len(args) else []
        self._repeat = 1

    def _parse(self, args: tuple[Self|Input|float|int|Hold|EndHold]) -> list[Self|Input]: pass

    def __add__(self, other: Self) -> Self:
        return Combo(self, other)

    def __mul__(self, other: int) -> Self:
        if (other < 0):
            raise ValueError("MUST BE POSITIVE INTEGER")
        elif (other == 1):
            return self
        else:
            combo = Combo()
            combo._pool = self._pool
            combo._repeat = self._repeat * other
            return combo

    def __rmul__(self, other: int) -> Self:
        return self * other

    def __str__(self):
        return f"Combo({", ".join(map(lambda x: str(x), self._pool))}){"" if self._repeat == 1 else f"*{self._repeat}"}"

    def hold(self, input: Input) -> Self:
        if isEmpty(input):
            return self
        else:
            combo = Combo()
            combo._pool = [x + input if isinstance(x, Input) else x.hold for x in self._pool]
            combo._repeat = self._repeat
            return combo

    def _send(self, previous: Input = EMPTY) -> Input:
        for _ in range(self._repeat):
            for x in self._pool:
                if type(x) is Input:
                    leftstick_changed = x._leftstick != previous._leftstick
                    rightstick_changed = x._rightstick != previous._rightstick

                    btns = x._buttons.state
                    hat = x._hatswitch.to_bytes()[0]
                    (lx, ly) = x._leftstick.to_bytes()
                    (rx, ry) = x._rightstick.to_bytes()

                    btns <<= 2
                    if leftstick_changed: btns |= 0x2
                    if rightstick_changed: btns |= 0x1

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

                    settings.python_command.keys.ser.ser.write(cmd)
                    # print(cmd)
                    time.sleep(x.seconds)
                    if isEmpty(x):
                        settings.python_command.checkIfAlive()

                    previous = x
                elif type(x) is Combo:
                    previous = x._send(previous)
                else:
                    raise Exception()
        return previous


def _parse(self, args: tuple[Combo|Input|float|int|Hold|EndHold]) -> list[Combo|Input]:
    ret: list[Combo | Input] = []
    input = EMPTY
    delay = 0.0
    auto_delay = 0.0
    for x in args:
        if isinstance(x, (int, float)):
            delay += x
        elif isinstance(x, Input):
            if delay or auto_delay:
                ret.append(Input(seconds=max(delay, auto_delay)) + input)
                delay = 0.0
            ret.append(x + input)
            auto_delay = settings.minimum_interval
        elif isinstance(x, Combo):
            if delay or auto_delay:
                ret.append(Input(seconds=max(delay, auto_delay)) + input)
                delay = 0.0
            if x._repeat != 1:
                ret.append(x.hold(input))
            else:
                ret += x.hold(input)._pool
            auto_delay = 0.0
        elif isinstance(x, Hold):
            input += x.input
        elif isinstance(x, EndHold):
            if (x.input):
                input -= x.input
            else:
                input = EMPTY
        elif x is EndHold:
            input = EMPTY
        else:
            raise ValueError(f"Illegal Argument: {x}")

    if delay or auto_delay:
        ret.append(Input(seconds=max(delay, auto_delay)))
    return ret

setattr(Combo, "_parse", _parse)

def send(*args: Self|Input|float|int|Hold|EndHold):
    combo = Combo()
    combo._pool = combo._parse(args)
    last = combo._send()
    if not isEmpty(last):
        Combo(EMPTY)._send(last)