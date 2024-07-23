from abc import ABC
import sys
from typing import Iterator, List, Tuple
from colorama import Back
from game.attempt import Attempt
from game.keyboard import Keyboard
from game.terminal_manipulator import ColoredString, ITerminalManipulator
from game.hint import *
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

UNDERLINE = "\033[4m"
END_UNDERLINE = "\033[0m"
COR_ERRADO = Back.LIGHTRED_EX
COR_CERTO = Back.GREEN
COR_POSICAO = Back.YELLOW
ENDC = Back.RESET

# CÒDIGOS PARA CORREÇÂO DE CADA LETRA
LETRA_DESCONHECIDA = -1
LETRA_INCORRETA = 0
POS_INCORRETA = 1
CERTO = 2

cores_das_dicas = {
    UNKNOWN_LETTER: ENDC,
    WRONG_LETTER: COR_ERRADO,
    WRONG_POS: COR_POSICAO,
    RIGHT_POS: COR_CERTO,
}

lim_chutes = 6


class IScreen(ABC):
    def __init__(self) -> None:
        pass

    def add(self, colored_string: ColoredString, pos: Tuple[int, int]):
        pass

    def __iter__(self):
        pass

    def __eq__(self, value: object) -> bool:
        pass


class Screen(IScreen):
    def __init__(self) -> None:
        self.strings = []

    def add(self, colored_string: ColoredString, pos: Tuple[int, int]) -> None:
        self.strings.append((colored_string, pos))

    def merge(self, other):
        if isinstance(other, self.__class__):
            for string, pos in other:
                self.add(string, pos)

    def __iter__(self) -> Iterator[Tuple[ColoredString, Tuple[int, int]]]:
        for string, pos in self.strings:
            yield string, pos

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            if len(self.strings) != len(other.strings):
                return False
            for (stringA, posA), (stringB, posB) in zip(self.strings, other.strings):
                if posA != posB:
                    return False
                if stringA != stringB:
                    return False
            return True
        return False


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
    def __init__(self, tmanipulator: ITerminalManipulator) -> None:
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
        self, tmanipulator: ITerminalManipulator, grid=None, offsets=None
    ) -> None:
        super().__init__(tmanipulator)
        self.tmanipulator = tmanipulator
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
            self.offsets = {"table": (0, 2), "keyboard": (10, 0)}

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
            if dica == WRONG_LETTER:
                dica = UNKNOWN_LETTER
            cores.append(dica)
        return cores

    def table_screen(self, challenge: IChallenge, challenge_number, lim_guesses):
        # table_offset = self.grid[challenge_number] + table_offset
        n = 0
        table_screen = Screen()
        for attempt in challenge.get_attempts():
            # pos = table_offset + (n, 0)
            pos = (n, 0)
            table_screen.add(self.format_attempt(attempt), pos)
            n += 1
        for i in range(n, lim_guesses):
            pos = self.grid[challenge_number]
            pos = (pos[0] + i, pos[1])
            table_screen.add(self.table_line(), pos)
        return table_screen

    def game_screen(self, challenges: List[IChallenge], lim_guesses=6) -> IScreen:

        game_screen = Screen()
        # table_offset = self.offsets["table"]
        for challenge_number, challenge in enumerate(challenges):
            game_screen.merge(
                self.table_screen(challenge, challenge_number, lim_guesses)
            )

            # pos = 0
            # game_screen.merge(self.keyboard(challenge.get_keyboard()), pos)
        return game_screen

    def table_line(self):
        return ColoredString("     ", [UNDERLINE for i in range(6)])

    def keyboard(self, keyboard: Keyboard, offset: Tuple[int, int]):
        keyboard_screen = Screen()
        pos = self.get_section_pos("keyboard", offset=offset)
        for line, line_number in keyboard:
            colored_line = self.format_keyboard_line(line)
            keyboard_screen.add(colored_line, (pos[0] + line_number, pos[1]))
        return keyboard_screen

    def format_keyboard_line(self, key_line: List[Tuple[str, Hint]]):
        string = ""
        hints = ""
        for char, hint in key_line:
            string += char
            hints.append(hint)
        colored_string = self.format_string_hints(string, hints)
        return colored_string

    def display_game_screen(self, challenges: List[IChallenge]):
        game_screen = self.game_screen(challenges)
        self.tmanipulator.print_screen(game_screen)


# class TerminalPresenter:
#     def __init__(self, lim_chutes: int, tmanipulator: ITerminalManipulator) -> None:
#         self.tmanipulator = tmanipulator

#         self.lim_chutes = lim_chutes
#         self.sections = {
#             "title": 0,
#             "table": 3,
#             "keyboard": 3 + lim_chutes + 1,
#             "messages": lim_chutes + 8,
#         }
#         self.padding = 2

#     ###########################################################################
#     ################           TELA PRINCIPAL              ####################
#     ###########################################################################

#     ################               CHUTES                  ####################

#     def display_at_pos(self, string: str, pos: Tuple[int, int] = (0, 0)):
#         self.tmanipulator.print_at_pos(string, pos)

#     def render_table_string(self):
#         table = ""
#         for i in range(self.lim_chutes):
#             table += self.render_table_line_string(i)
#         return table

#     def render_table_line_string(self, line):
#         string = self.empty_table_line()
#         pos = self.get_section_pos("table")
#         string = self.tmanipulator.string_at_pos(string, (pos[0] + line, pos[1]))
#         return string

#     def print_empty_table(self):
#         table_string = self.render_table_string()
#         self.display_at_pos(table_string)

#     def empty_table_line(self):
#         string = UNDERLINE + "     " + END_UNDERLINE
#         return string

#     def get_section_pos(self, section):
#         return (self.sections[section], self.padding)

#     def print_chutes(self, attempts):
#         pos = self.get_section_pos
#         for i, attempt in enumerate(attempts):
#             colored_attempt = self.color_attempt(attempt)
#             self.display_at_pos(colored_attempt, (pos[0] + i, pos[1]))

#     def color_attempt(self, attempt: Attempt):
#         chutes_colorido = ""
#         for letra, dica in attempt:
#             if dica == WRONG_LETTER:
#                 dica = UNKNOWN_LETTER
#             cor = cores_das_dicas[dica]
#             letra_colorida = f"{cor}{letra}{ENDC}"
#             chutes_colorido += letra_colorida
#         return chutes_colorido

#     #################                TECLADO                  ####################
#     def print_keyboard(self, linhas_teclado_dicas):
#         pos = (self.get_section_pos("keyboard"), self.padding)
#         for i, line in enumerate(linhas_teclado_dicas):
#             linha_colorida = self.color_keyboard_lines(line)
#             if i == 2:
#                 # A última linha começa uma casa depois por escolha de diagramação.
#                 linha_colorida = " " + linha_colorida
#             self.display_at_pos(linha_colorida, (pos[0] + i, pos[1]))

#     def color_keyboard_lines(self, linha_com_dicas):
#         linha_colorida = ""
#         for letra, dica in linha_com_dicas:
#             cor = cores_das_dicas[dica]
#             if cor == cores_das_dicas[WRONG_LETTER]:
#                 letra_colorida = " "
#             else:
#                 letra_colorida = f"{cor}{letra}{ENDC}"
#             linha_colorida += letra_colorida

#         return linha_colorida

#     ###########################################################################
#     ################                  GAME                 ####################
#     ###########################################################################

#     def print_game_at_pos(self, chutes, teclado_com_dicas, pos, feedbacks):
#         print(self.tmanipulator.go_to_pos(pos), end="")
#         sys.stdout.flush()
#         self.print_keyboard(teclado_com_dicas)
#         self.print_tabela(len(chutes))
#         self.print_chutes(chutes, feedbacks)
#         print(self.tmanipulator.go_to_pos((-pos[0], -pos[1])), end="")
#         sys.stdout.flush()
#         pass

#     ###########################################################################
#     ################               MENSAGENS               ####################
#     ###########################################################################

#     def message(self, mensagem):
#         self.tmanipulator.clear_line(lim_chutes + 6)
#         self.display_at_pos(mensagem, (lim_chutes + 6, 0))

#     def print_won_the_game(self, number_of_tries):
#         self.message(f"\rParabéns! Você acertou em {number_of_tries} tentativas!")
#         print(self.tmanipulator.go_to_pos((lim_chutes + 7, 0)))

#     def print_loss_the_game(self, desafios):
#         palavras_sorteadas = ""
#         for d in desafios:
#             palavras_sorteadas += " " + d.palavra
#         self.message(f"\rVocê perdeu. As palavras eram{palavras_sorteadas}.")
#         print(self.tmanipulator.go_to_pos((lim_chutes + 7, 0)))

#     def print_word_not_accepted(self, palavra):
#         self.message(f"Essa palavra não é aceita:{palavra}")

#     def first_print(self):
#         print("-------------O TERMO TERMINAL--------------")
#         print("versão para terminal de https://www.term.ooo")
#         # Limpa a tela
#         s = ""
#         for i in range(80):
#             s += " "
#         for i in range(lim_chutes + 7):
#             print(s)
#         print(f"\033[{lim_chutes + 7}A", end="")
#         sys.stdout.flush()

#         ###########################################################################
#         ###########################################################################
#         ################                                       ####################
#         ################                INPUTS                 ####################
#         ################                                       ####################
#         ###########################################################################
#         ###########################################################################

#     ###########################
#     def get_input(self, n, padding):
#         pos = (0, padding)
#         print(self.tmanipulator.go_to_pos(pos), end="")
#         self.tmanipulator.clear_line(n + 1)
#         self.print_tabela(n)
#         s = self.tmanipulator.go_to_pos((n + 1, 2))
#         chute_atual = unidecode(input(s)).upper()
#         print(self.tmanipulator.go_to_line(-n - 2), end="")
#         # print(self.tmanipulator.go_to_pos((-pos[0], -pos[1])), end="")
#         sys.stdout.flush()
#         return chute_atual
