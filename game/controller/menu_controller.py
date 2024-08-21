from abc import ABC
from typing import List, Tuple
from game.controller.controllercore import LEFTARROW, RIGHTARROW
from game.controller.icontroller import IController
from game.screen.iscreen_manager import IScreenManager


class IEndMatchMenuController(IController):
    def __init__(self) -> None:
        super().__init__()

    def process_key(self, key: str) -> None:
        pass


class IMenu(ABC):
    def __init__(self) -> None:
        super().__init__()

    def add_action_hook(self, action: function, button_id: str, action_id: str) -> None:
        pass

    def remove_action_hook(self, action_id: str) -> None:
        pass

    def move_focus(self, direction: int) -> None:
        pass

    def call_action_on_focus(self):
        pass

    # Maybe implement this using a with a special prefixed action id that would be set on menu creation?
    def end_menu(self):
        pass


class BaseMenu(IMenu):
    def __init__(self) -> None:
        super().__init__()

    def add_action_button_hook(
        self, action: function, button_id: str, action_id: str
    ) -> None:
        # Here should be a actual implementation of the function
        pass

    def set_action(self, action: function, action_id: int):
        pass

    def remove_action_hook(self, action_id: str) -> None:
        # Here should be a actual implementation of the function
        pass

    def move_focus(self, direction: int) -> None:
        # Here should be a actual implementation of the function
        pass

    def call_action_on_focus(self):
        # Here should be a actual implementation of the function
        pass

    def end_menu(self):
        # Here should be a actual implementation of the function
        pass


class MenuController(IController):
    def __init__(self, menu: IMenu) -> None:
        super().__init__()
        self.menu = menu

    def process_input(self, key: str) -> None:
        if ord(key) == 10:
            self.menu.call_action_on_focus()
        elif key == DOWNARROW:
            self.menu.move_focus(1)
        elif key == UPARROW:
            self.menu.move_focus(-1)
        elif ord(key) == 27:
            self.menu.end_menu()

    def start(self, match_screen: IScreen):
        self.menu.set_action(match_screen.set_focus, "RETURN")


class MenuBuilder:
    def __init__(self) -> None:
        pass

    def create(self):
        end_menu_controller = BaseMenu()


class GameSettings:
    def __init__(self) -> None:
        pass

    def get(self, setting_id):
        pass

    def set_config(self, value):
        pass


def start_new_game():
    n_games = GameSettings.get(None, "n_games")
    match_controller.new_match(n_games)


class MatchScreen(IScreen):
    def __init__(self, screen_manager: IScreenManager) -> None:
        super().__init__()
        self.screen_manager = screen_manager
        screen_manager.bind_screen(self, "match_screen")

    def process_key(self, key: str) -> None:
        exit(0)
