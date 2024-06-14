from time import sleep
import sys


def go_to_line(n):
    if n == 0:
        return ""
    elif n > 0:
        return f"\033[{n}B"
    else:
        return f"\033[{-n}A"


def go_to_char(n):
    if n == 0:
        return ""
    elif n > 0:
        return f"\033[{n}C"
    else:
        return f"\033[{-n}D"


def go_to_pos(pos):
    return go_to_char(pos[1]) + go_to_line(pos[0])


def print_at_pos(s, pos):
    padding_v = go_to_line(pos[0])
    padding_h = go_to_char(pos[1])
    end_v = go_to_line(-pos[0])
    end_h = go_to_char(-(pos[1] + len(s)))
    end = end_v + end_h
    # print(padding_h, end="")
    # sys.stdout.flush()
    print(padding_h + padding_v, end="")
    print(s, end=end)
    sys.stdout.flush()
    # print(end_h, end="")
    # sys.stdout.flush()
    # print(end_v, end="")
    # sys.stdout.flush()


def print_at_char(s, n):
    #    line = f"\033[{n[0]}"
    padding = f"\033[{n}C"
    end = f"\033[{n + len(s)}D"
    if n:
        print(padding + s, end=end)
    else:
        print(s, end=end)
    sys.stdout.flush()


c = "A"
for i in range(10):
    s = ""
    for n in range(10):
        s += c
    # print(s)
    print_at_pos(s, (i, i))
    c = chr(ord(c) + 1)
    sleep(1 / 8)
print("")
