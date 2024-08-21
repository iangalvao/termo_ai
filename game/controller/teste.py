from abc import ABC
import os
import sys
import select
import tty
import termios

LEFTARROW = "l"
RIGHTARROW = "r"
ESC = 27


class TerminalInputListener:
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
                    print("k:", k.encode("utf-8"), ord(k))
                    if k == "Q":
                        exit(0)
                    elif k == "\x1b":
                        print("waiting for data")
                        is_data = self.isData(0)
                        print("ISDATA:", is_data)
                        if is_data:
                            kk = os.read(sys.stdin.fileno(), 2).decode("utf-8")
                            print(
                                "ó o print:", kk.encode("utf-8"), ord(kk[0]), ord(kk[1])
                            )
                            if kk == "[C":
                                print("RIGHTARROW")
                            elif kk == "[D":
                                print(" LEFTARROW")
                        else:
                            print("ESC")

        finally:

            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            sys.stdout.write("\033[?25h")


til = TerminalInputListener()

while 1:
    til.get_input()
"""
What happens is that select.select returns a result if a file is ready for reading, but since we just used stdin.read(1), the file is flaged as not ready for reading. It thens enters in else part:
                      else:
                            print("ESC Key Detected")
                            # Handle ESC key action here
Prints ESC and restart the loop. When the loop restarts it waits for a new key and then print all the stdin buffer until reach the new key.
By thinking a little, i figure the implementation of select.select and maybe the underling os (ubuntu) is to mark a char as a start of a new input. Then if you only read one char and there is more to be read, it will be mark as not ready for reading by select.select. When a new input is found the file will be marked as ready to be read until the first char of the new input is read. After that, if something was left its doesnt mark the file as ready to be read.

That is what would explain the behavior i've seen, where checking for data in a non-blocking fashion always return false when searching for special escape chars. At the same time, when a new key is to be read in a blocking manner, it reads all that was left to be read from previous input until find the new char.

"""
