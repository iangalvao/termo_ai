from abc import ABC
import re
import sys
from typing import Tuple

from colorama import Back
from game.attempt import Attempt
from game.colored_string import ColoredString
from game.hint import *
from game.screen import IScreen, Screen


UNDERLINE = 3
ENDC = Back.RESET
COR_ERRADO = 0
COR_CERTO = 1
COR_POSICAO = 2


color_dict = {
    COR_ERRADO: Back.LIGHTRED_EX,
    COR_CERTO: Back.GREEN,
    COR_POSICAO: Back.YELLOW,
    ENDC: Back.RESET,
    UNDERLINE: "\033[4m",
}


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

    def print_screen(self, screen: IScreen):
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

    def print_colored_string_at_pos(
        self, colored_string: ColoredString, pos: Tuple[int]
    ):
        formatted_string = self.colored_string_at_pos(colored_string, pos)
        print(formatted_string, end="")
        sys.stdout.flush

    def colored_string_at_pos(self, colored_string: ColoredString, pos):
        formatted_string = self.color_string(colored_string)
        formatted_string = self.string_at_pos(formatted_string, pos)
        return formatted_string

    def print_screen(self, screen: Screen):
        for colored_string, pos in screen:
            self.print_colored_string_at_pos(colored_string, pos)

    def color_string(self, colored_string: ColoredString):
        formatted_string = ""
        for letter, color, _ in colored_string:
            color_ansi_code = self.color_dict[color]
            letra_colorida = f"{color_ansi_code}{letter}{ENDC}"
            formatted_string += letra_colorida
        return formatted_string
