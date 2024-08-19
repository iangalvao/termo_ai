from abc import ABC, abstractmethod
from argparse import Action
from typing import Any, Callable, Dict, List, Tuple
from game.controller.controllercore import (
    DELETE,
    DOWNARROW,
    LEFTARROW,
    RIGHTARROW,
    UPARROW,
)
from dataclasses import dataclass

from game.game_states.base_menu import BaseMenu
from game.game_states.end_match_menu import EndMatchMenu, MatchResult
from game.game_states.igame_context import IGameContext
from game.game_states.igame_state import IGameState
from game.game_states.menu import IMenu
from game.game_states.menustate import MenuState
from game.model.challenge import IChallenge
from game.viewer.game_display import IGameDisplay
from game.viewer.imenu_presenter import IMenuPresenter
from game.viewer.terminal_manipulator import IDisplayCore


# Not yet implemented
class MatchConfigState(MenuState):
    def __init__(self) -> None:
        pass


# Not yet implemented
class QuitState(MenuState):
    def __init__(self) -> None:
        pass


class IScreenManager(ABC):
    @abstractmethod
    def get_center(self) -> Tuple[int, int]:
        pass


class BaseMenuPresenter(IMenuPresenter):
    def __init__(self, screen_manager: IScreenManager, core: IDisplayCore) -> None:
        super().__init__()
        self.screen_manager: IScreenManager = screen_manager
        self.core: IDisplayCore = core

    def display_base_menu(self, menu: BaseMenu, base_pos):
        for i, action_id in enumerate(menu.actions_ids):
            pos = (base_pos[0] + i, base_pos[0])
            self.core.print_at_pos(action_id, pos)
            # this go on printing every action at one line, and highlightning the one in focus.

    def display_base_menu_frame(self, base_pos, size, height):
        frame = ""
        for i in range(size):
            frame += "*"
        self.core.print_at_pos(frame, base_pos)
        for i in range(height - 2):
            frame = "*"
            for i in range(size - 2):
                frame += " "
                frame += "*"
            self.core.print_at_pos(frame, (base_pos[0] + i, base_pos[1]))
        frame = ""
        for i in range(size):
            frame += "*"
        self.core.print_at_pos(frame, (base_pos[0] + height - 1, base_pos[1]))

    def display_menu(self, menu: IMenu) -> None:
        if isinstance(menu, BaseMenu):
            size = 40
            heigth = len(menu.actions_ids) + 4
            base_pos = self.screen_manager.get_center()
            base_pos = (base_pos[0] - (heigth + 1) // 2, base_pos[1] - size // 2)
            self.display_base_menu_frame(base_pos, size, heigth)
            self.display_base_menu(menu, base_pos)


class ScreenManager(IScreenManager):
    def __init__(self, height, width) -> None:
        super().__init__()
        self.height = height
        self.width = width

    def get_center(self) -> Tuple[int]:
        return (self.height, self.width)


class EndMatchMenuPresenter(BaseMenuPresenter):
    def __init__(self) -> None:
        super().__init__()

    def display_menu(self, menu: EndMatchMenu) -> None:
        results = EndMatchMenu.get_results()
        # Do something with result to print it...
        # something like:
        size = 50
        heigth = len(menu.actions_ids) + 6
        base_pos = self.screen_manager.get_center()
        base_pos = (base_pos[0] - (heigth + 1) // 2, base_pos[1] - size // 2)
        self.display_results(results, (base_pos[0] + 2, base_pos[1]))
        self.display_base_menu_frame(base_pos, size, heigth)
        self.display_base_menu(menu, (base_pos[0] + 4, base_pos[1]))

    def clear_menu(self) -> None:
        # If there is a area specific only for the menu, this should be implemented. Otherwise, not.
        pass

    def display_results(self, results: MatchResult, pos: Tuple[int, int]):
        if results.won:
            self.print_won_the_game(self, results.n_attempts, pos)
        else:
            self.print_loss_the_game(results.correct_words, pos)

    def message(self, mensagem: str, pos: Tuple[int, int]):
        self.tmanipulator.clear_line(self.lim_guesses + 6)
        self.tmanipulator.print_at_pos(mensagem, pos)

    def print_won_the_game(self, number_of_tries, pos: Tuple[int, int]):
        self.message(f"\rParabéns! Você acertou em {number_of_tries} tentativas!", pos)
        print(self.tmanipulator.go_to_pos((self.lim_guesses + 7, 0)))

    def print_loss_the_game(self, desafios, pos: Tuple[int, int]):
        if len(desafios) == 1:
            self.message(f"\rVocê perdeu. A palavra era {desafios[0].palavra}.", pos)
        else:
            palavras_sorteadas = ""
            for d in desafios:
                palavras_sorteadas += " " + d.palavra
            self.message(f"\rVocê perdeu. As palavras eram{palavras_sorteadas}.", pos)
        print(self.tmanipulator.go_to_pos((self.lim_guesses + 7, 0)))
