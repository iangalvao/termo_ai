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

    def isData():
        return select.select([sys.stdin], [], []) == ([sys.stdin], [], [])

    def listen(self):
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())

            while 1:
                if self.isData():
                    k = sys.stdin.read(1)
                    if k == "q":
                        break
                    elif k == "\x1b":
                        kk = sys.stdin.read(2)
                        if kk == "[C":
                            return RIGHTARROW
                        elif kk == "[D":
                            return LEFTARROW
                        else:
                            print(
                                "unidecode escape char pressed -->",
                                kk.encode("unicode_escape"),
                            )
                    elif ord("a") <= ord(k) <= ord("z"):
                        yield k
                    elif ord(k) == 10 or ord(k) == 13:
                        return ENTER
                    else:
                        print("unknown char pressed: ", k)

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
