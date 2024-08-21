from abc import ABC
import os
import sys
import select
import tty
import termios

ENTER = 0
LEFTARROW = "l"
DOWNARROW = "2"
UPARROW = "8"
RIGHTARROW = "r"
DELETE = "d"
ESC = "\x1b"


class IInputListener(ABC):
    def __init__(self) -> None:
        super().__init__()

    def get_input(self) -> str:
        pass


class TerminalInputListener(IInputListener):
    def __init__(self):
        pass

    def isData(self, block=True):
        if block:
            return select.select([sys.stdin], [], []) == ([sys.stdin], [], [])
        else:
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    def get_input(self):
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            print("\033[?25l", end="")
            sys.stdout.flush()
            tty.setcbreak(sys.stdin.fileno())

            while 1:
                if self.isData():
                    k = os.read(sys.stdin.fileno(), 1).decode("utf-8")
                    if k == "Q":
                        exit(0)
                    elif k == "\x1b":
                        if self.isData(0):
                            kk = os.read(sys.stdin.fileno(), 2).decode("utf-8")
                            if kk == "[C":
                                return RIGHTARROW
                            elif kk == "[D":
                                return LEFTARROW
                            elif kk == "[A":
                                return UPARROW
                            elif kk == "[B":
                                return DOWNARROW
                            elif kk == "[3":
                                return DELETE
                        else:
                            return ESC
                    else:
                        if k.isalpha():
                            return k.upper()
                        return k
        finally:

            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            sys.stdout.write("\033[?25h")
