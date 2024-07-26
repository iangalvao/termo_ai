import sys
import select
import tty
import termios


def isData():
    return select.select([sys.stdin], [], []) == ([sys.stdin], [], [])


old_settings = termios.tcgetattr(sys.stdin)
try:
    tty.setcbreak(sys.stdin.fileno())

    while 1:
        if isData():
            k = sys.stdin.read(1)
            if k == "q":
                break
            elif k == "\x1b":
                kk = sys.stdin.read(2)
                if kk == "[A":
                    print("up")
                elif kk == "[B":
                    print("down")
                elif kk == "[C":
                    print("right")
                elif kk == "[D":
                    print("left")

                print("-->", k.encode("unicode_escape"), ord(k), end=" ; ")
                for c in kk:
                    print(c.encode("unicode_escape"), ord(c), end=" ; ")
                print("")
            elif ord("a") <= ord(k) <= ord("z"):
                print(k, ord(k))
            else:
                print("char pressed: ", k.encode("unicode_escape"), ord(k))

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
