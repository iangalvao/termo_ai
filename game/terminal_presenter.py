from abc import ABC
import re
import sys
from typing import Tuple


class IPresenter(ABC):
    def __init__(self) -> None:
        super().__init__()

    def go_to_pos(self, pos: Tuple[int,int]):
        pass

    def print_at_pos(self, s: str, pos: Tuple[int, int]) -> None:
        pass

    def clear_line(self, n: int) -> None:
        pass

class TerminalPresenter(IPresenter):
    def __init__(self, line_length = 75) -> None:
        super().__init__()
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
        ansi_escape = re.compile(r'\033\[[0-9;]*m')
        
        # Remove ANSI escape sequences from the string
        clean_string = ansi_escape.sub('', s)
        # Count visible characters (letters, numbers, spaces, and punctuation)
        count = sum(1 for char in clean_string if char.isprintable())
        
        return count

    def string_at_pos(self, s: str, pos: tuple[int, int]) -> str:
        forward = self.go_to_pos(pos)
        backward = self.go_to_pos((-pos[0], -pos[1] - self.string_size(s)))
        return forward + s + backward


    def clean_line_at_pos(self, pos: int) -> str:
        clean_line_string = " " * self.line_length
        return self.string_at_pos(clean_line_string, (pos, 0))


    def clear_line(self, s: str, pos: int) -> None:
        string_to_print = self.clean_line_at_pos(pos)
        print(string_to_print)
        sys.stdout.flush()
    
    def print_at_pos(self, s: str, pos: tuple[int, int]) -> None:
        string_to_print = self.string_at_pos(s, pos)
        print(string_to_print)
        sys.stdout.flush()
        