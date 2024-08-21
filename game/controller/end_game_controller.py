from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Tuple
from game.controller.controllercore import (
    DELETE,
    DOWNARROW,
    LEFTARROW,
    RIGHTARROW,
    UPARROW,
)
from dataclasses import dataclass

from game.game_states.action import Action
from game.game_states.base_menu import BaseMenu
from game.game_states.end_match_menu import EndMatchMenu, MatchResult
from game.game_states.igame_context import IGameContext
from game.game_states.igame_state import IGameState
from game.game_states.menu import IMenu
from game.game_states.menustate import MenuState
from game.model.challenge import IChallenge
from game.viewer.colored_string import ColoredString
from game.viewer.game_display import IGameDisplay
from game.viewer.imenu_presenter import IMenuPresenter
from game.viewer.terminal_manipulator import COR_CERTO, COR_INVERTIDA, IDisplayCore


# Not yet implemented
class MatchConfigState(MenuState):
    def __init__(self, presenter: IMenuPresenter) -> None:
        super().__init__(presenter)

    def on_enter(self, context) -> None:
        self.menu = BaseMenu()

        self.menu.set_action(
            Action(
                context.change_state,
                state_id="play_state",
                n_challenges=1,
            ),
            "1",
        )

        self.menu.set_action(
            Action(
                context.change_state,
                state_id="play_state",
                n_challenges=2,
            ),
            "2",
        )
        self.menu.set_action(
            Action(
                context.change_state,
                state_id="play_state",
                n_challenges=3,
            ),
            "3",
        )
        self.menu.set_action(
            Action(context.change_state, state_id="main_menu_state"), "back"
        )
        self.presenter.display_menu(self.menu)


# Not yet implemented
class QuitState(MenuState):
    def __init__(self, presenter: IMenuPresenter) -> None:
        super().__init__(presenter)

    def on_enter(self, context, previous_state) -> None:
        self.previous_state = previous_state
        self.presenter.message("Press Any Key to Quit. ESC to cancel.", (21, 0))

    def on_exit(self, context: IGameContext) -> None:
        pass

    def handle_input(self, context: IGameContext, key: str) -> None:
        if ord(key) == 27:
            context.change_state(self.previous_state)

            self.presenter.message(" " * 40, (21, 0))
            return
        self.presenter.quit()
        exit(0)


class IScreenManager(ABC):
    @abstractmethod
    def get_center(self) -> Tuple[int, int]:
        pass


class BaseMenuPresenter(IMenuPresenter):
    def __init__(self, screen_manager: IScreenManager, core: IDisplayCore) -> None:
        super().__init__()
        self.screen_manager: IScreenManager = screen_manager
        self.core: IDisplayCore = core

    def display_base_menu(self, menu: BaseMenu, base_pos, width):
        for i, action_id in enumerate(menu.actions_ids):
            pos = (base_pos[0] + 2 + i, base_pos[1] + 4)
            if i == menu.focus:
                s = action_id + " " * (width - len(action_id))
                self.core.print_at_pos(action_id, pos)
                self.core.print_colored_string_at_pos(
                    ColoredString(s, [COR_INVERTIDA for l in s]), pos
                )
            else:
                self.core.print_at_pos(action_id, pos)
            # this go on printing every action at one line, and highlightning the one in focus.

    def display_base_menu_frame(self, base_pos, size, height):
        frame = ""
        for i in range(size):
            frame += "*"

        self.core.print_at_pos(frame, base_pos)
        for i in range(height - 1):
            frame = "*"
            for j in range(size - 2):
                frame += " "
            frame += "*"
            self.core.print_at_pos(frame, (base_pos[0] + 1 + i, base_pos[1]))
        frame = ""
        for i in range(size):
            frame += "*"

        self.core.print_at_pos(frame, (base_pos[0] + height - 1, base_pos[1]))

    def display_menu(self, menu: IMenu) -> None:
        # if isinstance(menu, BaseMenu):
        size = 40
        heigth = len(menu.actions_ids) + 4
        base_pos = self.screen_manager.get_center()
        base_pos = (base_pos[0] - (heigth + 1) // 2, base_pos[1] - size // 2)
        self.clear_menu()
        self.display_base_menu_frame(base_pos, size, heigth)
        self.display_base_menu(menu, base_pos, size - 8)

    def clear_menu(self) -> None:
        # If there is a area specific only for the menu, this should be implemented. Otherwise, not.
        s = ""
        for _ in range(self.screen_manager.width):
            s += " "
        for i in range(2, self.screen_manager.height):
            self.core.print_at_pos(s, (i, 0))

    def message(self, mensagem: str, pos: Tuple[int, int]):
        # self.core.clear_line((pos[0]))
        self.core.print_at_pos(mensagem, pos)


class ScreenManager(IScreenManager):
    def __init__(self, height=24, width=80) -> None:
        super().__init__()
        self.height = height
        self.width = width

    def get_center(self) -> Tuple[int]:
        return (self.height // 2, self.width // 2)


class EndMatchMenuPresenter(BaseMenuPresenter):
    def __init__(self, screen_manager: IScreenManager, core: IDisplayCore) -> None:
        super().__init__(screen_manager, core)

    def display_menu(self, menu: EndMatchMenu) -> None:
        results = menu.results
        size = 50
        heigth = len(menu.actions_ids) + 6
        base_pos = self.screen_manager.get_center()
        base_pos = (base_pos[0] - (heigth + 1) // 2, base_pos[1] - size // 2)
        self.display_base_menu_frame((base_pos[0] - 2, base_pos[1]), size, heigth + 3)
        self.display_results(results, (base_pos[0] + 2, base_pos[1] + 4))
        self.display_base_menu(menu, (base_pos[0] + 2, base_pos[1]), size - 8)

    def display_results(self, results: MatchResult, pos: Tuple[int, int]):
        if results.won:
            self.print_won_the_game(results.n_attempts, pos)
        else:
            self.print_loss_the_game(results.correct_words, pos)

    def message(self, mensagem: str, pos: Tuple[int, int]):
        # self.core.clear_line((pos[0]))
        self.core.print_at_pos(mensagem, pos)

    def print_won_the_game(self, number_of_tries, pos: Tuple[int, int]):
        self.message(f"Parabéns! Você acertou em {number_of_tries} tentativas!", pos)
        # print(self.core.go_to_pos(pos))

    def print_loss_the_game(self, desafios: List[IChallenge], pos: Tuple[int, int]):
        if len(desafios) == 1:
            self.message(f"Você perdeu. A palavra era {desafios[0]}.", pos)
        else:
            palavras_sorteadas = ""
            for d in desafios:
                palavras_sorteadas += " " + d
            self.message(f"\rVocê perdeu. As palavras eram{palavras_sorteadas}.", pos)
        # print(self.core.go_to_pos(pos))


class QuitPresenter(BaseMenuPresenter):
    def __init__(self, screen_manager: IScreenManager, core: IDisplayCore) -> None:
        super().__init__(screen_manager, core)

    def quit(self):
        print(self.core.go_to_pos((24, 80)))
