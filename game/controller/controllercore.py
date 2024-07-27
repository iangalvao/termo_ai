from abc import ABC
import sys
import select
import tty
import termios

ENTER = 0
LEFTARROW = "l"
RIGHTARROW = "r"
DELETE = "d"


class IInputListener(ABC):
    def __init__(self) -> None:
        super().__init__()

    def get_input(self) -> str:
        pass


class TerminalInputListener(IInputListener):
    def __init__(self):
        pass

    def isData(self):
        return select.select([sys.stdin], [], []) == ([sys.stdin], [], [])

    def get_input(self):
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            print("\033[?25l", end="")
            sys.stdout.flush()
            tty.setcbreak(sys.stdin.fileno())

            while 1:
                if self.isData():
                    k = sys.stdin.read(1)
                    if k == "Q":
                        exit(0)
                    elif k == "\x1b":
                        kk = sys.stdin.read(2)
                        if kk == "[C":
                            return RIGHTARROW
                        elif kk == "[D":
                            return LEFTARROW
                        elif kk == "[3":
                            return DELETE
                    else:
                        if k.isalpha():
                            return k.upper()
                        return k
        finally:

            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            sys.stdout.write("\033[?25h")
