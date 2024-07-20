from abc import ABC
import re
import sys
from typing import Tuple

from colorama import Back
from game.attempt import Attempt
from game.hint import *

bcolors = {
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKCYAN": "\033[96m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
}

# CÒDIGOS PARA CORREÇÂO DE CADA LETRA
LETRA_DESCONHECIDA = -1
LETRA_INCORRETA = 0
POS_INCORRETA = 1
CERTO = 2


UNDERLINE = "\033[4m"
ENDC = Back.RESET
COR_ERRADO = 0
COR_CERTO = 1
COR_POSICAO = 2


color_dict = {
    COR_ERRADO: Back.LIGHTRED_EX,
    COR_CERTO: Back.GREEN,
    COR_POSICAO: Back.YELLOW,
    ENDC: Back.RESET,
}


class ColoredString:
    def __init__(self, string, colors) -> None:
        self.str = string
        self.colors = colors

    def __iter__(self):
        for pos, letter_and_color in enumerate(zip(self.str, self.colors)):
            yield letter_and_color[0], letter_and_color[1], pos


class ITerminalManipulator(ABC):
    def __init__(self) -> None:
        super().__init__()

    def go_to_pos(self, pos: Tuple[int, int]) -> str:
        pass

    def print_at_pos(self, s: str, pos: Tuple[int, int]) -> None:
        pass

    def print_colored_string(self, colored_string: ColoredString, pos: Tuple[int, int]):
        pass

    def clear_line(self, n: int) -> None:
        pass


class TerminalManipulator(ITerminalManipulator):
    def __init__(self, color_dict, line_length=75) -> None:
        super().__init__()
        self.color_dict = color_dict
        self.line_length = line_length

    def go_to_line(self, n):
        if n == 0:
            return ""
        elif n > 0:
            return f"\033[{n}B"
        else:
            return f"\033[{-n}A"

    def go_to_char(self, n):
        if n == 0:
            return ""
        elif n > 0:
            return f"\033[{n}C"
        else:
            return f"\033[{-n}D"

    def go_to_pos(self, pos):
        return self.go_to_line(pos[0]) + self.go_to_char(pos[1])

    def string_size(self, s: str) -> int:
        # Regular expression to match ANSI escape sequences
        ansi_escape = re.compile(r"\033\[[0-9;]*[m,C]")

        # Remove ANSI escape sequences from the string
        clear_string = ansi_escape.sub("", s)
        # Count visible characters (letters, numbers, spaces, and punctuation)
        count = sum(1 for char in clear_string if char.isprintable())

        return count

    def string_at_pos(self, s: str, pos: Tuple[int, int]) -> str:
        forward = self.go_to_pos(pos)
        backward = self.go_to_pos((-pos[0], -pos[1] - self.string_size(s)))
        return forward + s + backward

    def clear_line_at_pos(self, pos: int) -> str:
        clear_line_string = " " * self.line_length
        return self.string_at_pos(clear_line_string, (pos, 0))

    def clear_line(self, pos: int) -> None:
        string_to_print = self.clear_line_at_pos(pos)
        print(string_to_print, end="")
        sys.stdout.flush()

    def print_at_pos(self, s: str, pos: Tuple[int, int]) -> None:
        string_to_print = self.string_at_pos(s, pos)
        print(string_to_print, end="")
        sys.stdout.flush()

    def colored_string_at_pos(self, colored_string: ColoredString, pos):
        formatted_string = self.color_string(colored_string)
        formatted_string = self.string_at_pos(formatted_string, pos)
        return formatted_string

    def color_string(self, colored_string: ColoredString):
        formatted_string = ""
        for letter, color, _ in colored_string:
            color_ansi_code = self.color_dict[color]
            letra_colorida = f"{color_ansi_code}{letter}{ENDC}"
            formatted_string += letra_colorida
        return formatted_string
