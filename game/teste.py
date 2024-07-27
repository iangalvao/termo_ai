import select
import sys
import termios
import tty


def isData():
    return select.select([sys.stdin], [], []) == ([sys.stdin], [], [])


def get_input():
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        print("\033[?25l", end="")
        sys.stdout.flush()
        tty.setcbreak(sys.stdin.fileno())

        while 1:
            if isData():
                k = sys.stdin.read(1)
                if k == "Q":
                    exit(0)
                elif k == "\x1b":
                    kk = sys.stdin.read(2)
                    if kk == "[C":
                        return
                    elif kk == "[D":
                        return
                    for c in kk:
                        print(c.encode("utf-8"), ord(c))

                print(k.encode("utf-8"), ord(k))

    finally:

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        sys.stdout.write("\033[?25h")


get_input()
