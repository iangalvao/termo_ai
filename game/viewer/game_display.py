from abc import ABC, abstractmethod
import sys
from typing import  List, Tuple
from game.model.attempt import Attempt
from game.game_engine.buffer import Buffer
from game.model.hint import RIGHT_POS, UNKNOWN_LETTER, WRONG_LETTER, WRONG_POS, Hint
from game.model.keyboard import Keyboard
from game.model.challenge import IChallenge
from game.model.imatch import IMatch
from game.game_engine.presenters.colored_string import ColoredString
from game.game_engine.presenters.screen import IScreen, Screen

from game.game_engine.presenters.terminal_manipulator import COR_CERTO, COR_ERRADO, COR_INVERTIDA, COR_POSICAO, ENDC, UNDERLINE, IDisplayCore

# CORES PARA VISUALIZAÇÂO NO TERMINAL
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


cores_das_dicas = {
    UNKNOWN_LETTER: ENDC,
    WRONG_LETTER: COR_ERRADO,
    WRONG_POS: COR_POSICAO,
    RIGHT_POS: COR_CERTO,
}


class Message:
    def __init__(self) -> None:
        pass


class IGameDisplay(ABC):
    def __init__(self, tmanipulator: IDisplayCore) -> None:
        super().__init__()
        
    @abstractmethod
    def display_game_screen(self, match: IMatch, buffer: Buffer) -> None:
        pass

    @abstractmethod
    def print_word_not_accepted(self, palavra:str) -> None:
        pass
    
    @abstractmethod
    def first_print(self) -> None:
        pass
    @abstractmethod
    def start(self, n_challenges: int) -> None:
        pass
    
class TerminalPresenter(IGameDisplay):
    def __init__(
        self, tmanipulator: IDisplayCore, lim_chutes=6, grid=None, offsets=None
    ) -> None:
        super().__init__(tmanipulator)
        self.tmanipulator = tmanipulator
        self.lim_guesses = lim_chutes
        if not grid:
            self.grid = [(3, 0)]
        else:
            if isinstance(grid, int):
                self.grid = [(x, 0) for x in range(0, grid, 25)]
            else:
                self.grid = grid
        if offsets:
            self.offsets = offsets
        else:
            self.offsets = {"table": (1, 6), "keyboard": (2, 4)}

    def format_attempt(self, attempt: Attempt):
        string = attempt.get_guess()
        hints = attempt.get_feedbacks()
        return self.format_string_hints(string, hints)

    def format_string_hints(self, string: str, hints: List[Hint]):
        colors = self.colors_from_hints(hints)
        colored_string = ColoredString(string, colors)
        return colored_string

    def colors_from_hints(self, hints: List[Hint]):
        cores = []
        for dica in hints:
            cores.append(cores_das_dicas[dica])
        return cores

    def table_screen(self, challenge: IChallenge, challenge_number, lim_guesses):
        game_pos = self.grid[challenge_number]
        table_offset = self.get_section_pos("table", game_pos)
        n = 0
        table_screen = Screen()
        for attempt in challenge.get_attempts():
            pos = (table_offset[0] + n, table_offset[1])
            table_screen.add(self.format_attempt(attempt), pos)
            n += 1
        for i in range(n, lim_guesses):
            pos = (table_offset[0] + i, table_offset[1])
            table_screen.add(self.table_line(), pos)
        return table_screen

    def game_screen(self, match: IMatch) -> IScreen:
        challenges = match.get_challenges()
        lim_guesses = len(challenges) + 5
        game_screen = Screen()
        # table_offset = self.offsets["table"]
        for challenge_number, challenge in enumerate(challenges):
            game_screen.merge(
                self.table_screen(challenge, challenge_number, lim_guesses)
            )
            game_pos = self.grid[challenge_number]
            keyboard_pos = self.get_section_pos(
                "keyboard", (game_pos[0] + lim_guesses, game_pos[1])
            )
            game_screen.merge(self.keyboard(challenge.get_keyboard(), keyboard_pos))
        return game_screen

    def table_line(self):
        return ColoredString("     ", [UNDERLINE for i in range(6)])

    def get_section_pos(self, section: str, offset: Tuple[int, int]):
        section_offset = self.offsets[section]
        return (section_offset[0] + offset[0], section_offset[1] + offset[1])

    def keyboard(self, keyboard: Keyboard, offset: Tuple[int, int]):
        keyboard_screen = Screen()
        for line, line_number in keyboard:
            colored_line = self.format_keyboard_line(line)
            keyboard_screen.add(colored_line, (offset[0] + line_number, offset[1]))
        return keyboard_screen

    def format_keyboard_line(self, key_line: List[Tuple[str, Hint]]):
        string = ""
        hints = []
        for char, hint in key_line:
            hints.append(hint)
            if hint == WRONG_LETTER:
                string += " "
            else:
                string += char

        colored_string = self.format_string_hints(string, hints)
        return colored_string

    def display_game_screen(self, match: IMatch, buffer: Buffer) -> None:
        game_screen = self.game_screen(match)
        self.tmanipulator.print_screen(game_screen)
        self.display_buffer(buffer, match.get_n_attempts() + 1, match.get_challenges(), buffer.cursor_position)
        
    def display_buffer(self, buffer, line, challenges, cursor):
        if line >= self.lim_guesses:
            return
        for challenge_number, challenge in enumerate(challenges):
            tmp_buffer = buffer + " "
            game_pos = self.grid[challenge_number]
            table_offset = self.get_section_pos("table", game_pos)
            pos = (table_offset[0] + line, table_offset[1])
            colors = [UNDERLINE for i in tmp_buffer]
            colors[-1] = ENDC
            colors[cursor] = COR_INVERTIDA
            colored_string = ColoredString(tmp_buffer, colors)
            buffer_screen = Screen()
            buffer_screen.add(colored_string, pos)
            self.tmanipulator.print_screen(buffer_screen)

    def message(self, mensagem):
        self.tmanipulator.clear_line(self.lim_guesses + 6)
        self.tmanipulator.print_at_pos(mensagem, (self.lim_guesses + 8, 0))

    def print_word_not_accepted(self, palavra):
        self.message(f"Essa palavra não é aceita:{palavra}")

    def first_print(self):
        # clear screen
        s = ""
        for i in range(80): # TODO replace literals by screen_manager width and height
            s += " "
        for j in range(2, 22):
            self.tmanipulator.print_at_pos(s, (j, 0))
        # self.tmanipulator.print_at_pos(
        #    "-------------O TERMO TERMINAL--------------", (0, 0)
        # )
        # self.tmanipulator.print_at_pos(
        #    "versão para terminal de https://www.term.ooo", (1, 0)
        # )
        sys.stdout.flush()

    def start(self, n_challenges: int) -> None:
        self.grid = [(2, 11 * i) for i in range(n_challenges)]