from abc import ABC, abstractmethod
import os
import sys
import select
import tty
import termios

LEFTARROW = "l"
RIGHTARROW = "r"
ESC = 27


class IInputListener(ABC):
    def __init__(self) -> None:
        super().__init__()
    @abstractmethod
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
                                print("RIGHTARROW")
                            elif kk == "[D":
                                print("LEFTARROW")
                            elif kk == "[A":
                                print("UPARROW")
                            elif kk == "[B":
                                print("DOWNARROW")
                            elif kk == "[3":
                                print("DELETE")
                            elif kk == "[<":
                                self.handle_mouse_input()
                        else:
                            print("ESC")
                    else:
                        if k.isalpha():
                            return k.upper()
                        return k

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            sys.stdout.write("\033[?25h")

    def handle_mouse_input(self):

        while self.isData(0):
            k = os.read(sys.stdin.fileno(), 1).decode("utf-8")
            print("k:", k.encode("utf-8"), ord(k))


til = TerminalInputListener()

while 1:
    til.get_input()
