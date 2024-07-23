from abc import ABC
import sys
from typing import Iterator, List, Tuple
from colorama import Back
from game.model.attempt import Attempt
from game.model.keyboard import Keyboard
from game.viewer.screen import IScreen, Screen
from game.viewer.terminal_manipulator import *
from game.model.hint import *
from unidecode import unidecode

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


class IKeyboard(ABC):
    def __init__(self) -> None:
        super().__init__()


class Message:
    def __init__(self) -> None:
        pass


class IChallenge:
    def __init__(self) -> None:
        pass

    def get_attempts(self) -> List[Attempt]:
        pass

    def get_lim_guesses(self) -> int:
        pass

    def get_keyboard(self) -> IKeyboard:
        pass


class IGameDisplay(ABC):
    def __init__(self, tmanipulator: IDisplayCore) -> None:
        super().__init__()

    def display_challenge(self, challenge: IChallenge, pos: Tuple[int]) -> None:
        pass

    def display_intro(self) -> None:
        pass

    def display_message(self, message: Message) -> None:
        pass

    def display_game_screen(self, challenges: List[IChallenge]):
        pass


class TerminalPresenter(IGameDisplay):
    def __init__(
        self, tmanipulator: IDisplayCore, lim_chutes=6, grid=None, offsets=None
    ) -> None:
        super().__init__(tmanipulator)
        self.tmanipulator = tmanipulator
        self.lim_chutes = lim_chutes
        if not grid:
            self.grid = [(0, 0)]
        else:
            if isinstance(grid, int):
                self.grid = [(x, 0) for x in range(0, grid, 25)]
            else:
                self.grid = grid
        if offsets:
            self.offsets = offsets
        else:
            self.offsets = {"table": (1, 6), "keyboard": (2 + lim_chutes, 4)}

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
        # table_offset = self.grid[challenge_number] + table_offset
        n = 0
        table_screen = Screen()
        for attempt in challenge.get_attempts():
            pos = (table_offset[0] + n, table_offset[1])
            table_screen.add(self.format_attempt(attempt), pos)
            n += 1
        for i in range(n, self.lim_chutes):
            pos = (table_offset[0] + i, table_offset[1])
            table_screen.add(self.table_line(), pos)
        return table_screen

    def game_screen(self, challenges: List[IChallenge], lim_guesses=6) -> IScreen:

        game_screen = Screen()
        # table_offset = self.offsets["table"]
        for challenge_number, challenge in enumerate(challenges):
            game_screen.merge(
                self.table_screen(challenge, challenge_number, lim_guesses)
            )
            game_pos = self.grid[challenge_number]
            keyboard_pos = self.get_section_pos("keyboard", game_pos)
            game_screen.merge(self.keyboard(challenge.get_keyboard(), keyboard_pos))
        return game_screen

    def table_line(self):
        return ColoredString("_____", [ENDC for i in range(6)])

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

    def display_game_screen(self, challenges: List[IChallenge]):
        game_screen = self.game_screen(challenges)
        self.tmanipulator.print_screen(game_screen)

    ###########################################################################
    ################               MENSAGENS               ####################
    ###########################################################################

    def message(self, mensagem):
        self.tmanipulator.clear_line(self.lim_chutes + 6)
        self.tmanipulator.print_at_pos(mensagem, (self.lim_chutes + 6, 0))

    def print_won_the_game(self, number_of_tries):
        self.message(f"\rParabéns! Você acertou em {number_of_tries} tentativas!")
        print(self.tmanipulator.go_to_pos((self.lim_chutes + 7, 0)))

    def print_loss_the_game(self, desafios):
        if len(desafios) == 1:
            self.message(f"\rVocê perdeu. A palavra era {desafios[0].palavra}.")
        else:
            palavras_sorteadas = ""
            for d in desafios:
                palavras_sorteadas += " " + d.palavra
            self.message(f"\rVocê perdeu. As palavras eram{palavras_sorteadas}.")
        print(self.tmanipulator.go_to_pos((self.lim_chutes + 7, 0)))

    def print_word_not_accepted(self, palavra):
        self.message(f"Essa palavra não é aceita:{palavra}")

    def first_print(self):
        print("-------------O TERMO TERMINAL--------------")
        print("versão para terminal de https://www.term.ooo")
        # Limpa a tela
        s = ""
        for i in range(80):
            s += " "
        for i in range(self.lim_chutes + 7):
            print(s)
        print(f"\033[{self.lim_chutes + 7}A", end="")
        sys.stdout.flush()

        ###########################################################################
        ###########################################################################
        ################                                       ####################
        ################                INPUTS                 ####################
        ################                                       ####################
        ###########################################################################
        ###########################################################################

    ###########################
    def get_input(self, n, padding):
        pos = (0, padding)
        print(self.tmanipulator.go_to_pos(pos), end="")
        self.tmanipulator.clear_line(n + 1)
        # self.print_tabela(n)
        s = self.tmanipulator.go_to_pos((n + 1, 2))
        chute_atual = unidecode(input(s)).upper()
        print(self.tmanipulator.go_to_line(-n - 2), end="")
        # print(self.tmanipulator.go_to_pos((-pos[0], -pos[1])), end="")
        sys.stdout.flush()
        return chute_atual
