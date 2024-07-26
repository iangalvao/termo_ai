from abc import ABC
import sys
import select
import tty
import termios

ENTER = 0
LEFTARROW = 1
RIGHTARROW = 2


class IInputListener(ABC):
    def __init__(self) -> None:
        super().__init__()

    def listen(self) -> str:
        pass


class TerminalInputListener(IInputListener):
    def __init__(self):
        pass

    def isData(self):
        return select.select([sys.stdin], [], []) == ([sys.stdin], [], [])

    def get_input(self):
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())

            while 1:
                if self.isData():
                    k = sys.stdin.read(1)
                    if k == "Q":
                        break
                    elif k == "\x1b":
                        kk = sys.stdin.read(2)
                        if kk == "[C":
                            return RIGHTARROW
                        elif kk == "[D":
                            return LEFTARROW
                    else:
                        return k.upper()

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
