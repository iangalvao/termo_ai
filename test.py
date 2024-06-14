from time import sleep


def go_to_line(n):
    s = ""
    for i in range(n):
        s += "\n"
    return s


def go_to_pos(n):
    s = ""
    for i in range(n):
        s += " "
    return s


def print_at_pos(string, pos):
    s = ""
    s += go_to_line(pos[0])
    s += go_to_pos(pos[1])
    s += string
    if pos[0] > 0:
        print(s, end=f"\033[{pos[0]}A\r")
    else:
        print(s, end="\r")


def first_print():
    print("-------------O TERMO TERMINAL--------------")
    print("versão para terminal de https://www.term.ooo")
    s = ""
    for i in range(6):
        print_at_pos("AAAAA", (1 + i, 18))

    print("\n\n\r", end="\033[2A\r")
    sleep(1 / 2)
    print("BBBBB", end="\r")
    print_at_pos("CCCCC", (1, 18))
    sleep(1 / 2)
    print_at_pos("DDDDD", (2, 18))
    sleep(1 / 2)
    print_at_pos("EEEEE", (3, 18))
    sleep(1 / 2)
    print_at_pos("FFFFF", (4, 18))
    sleep(1 / 2)
    print_at_pos("GGGGG", (5, 18))


def clean_line(n):
    s = ""
    for i in range(80):
        s += " "
    print_at_pos(s, (n, 0))


first_print()
