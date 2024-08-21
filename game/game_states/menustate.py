# This class does not implement on_enter abstract method. Thus, is a incomplete implementation,
# intended to be used only as a base for other menu states
from game.controller.controllercore import DOWNARROW, ESC, UPARROW
from game.game_states.igame_context import IGameContext
from game.game_states.igame_state import IGameState
from game.game_states.menu import IMenu
from game.viewer.imenu_presenter import IMenuPresenter


class MenuState(IGameState):
    def __init__(self, presenter: IMenuPresenter) -> None:
        super().__init__()
        self.menu: IMenu = None
        self.presenter: IMenuPresenter = presenter

    def handle_input(self, context: IGameContext, key: str) -> None:
        if ord(key) == 10:
            self.menu.call_action_on_focus()
            return
        elif key == DOWNARROW:
            self.menu.move_focus(1)
        elif key == UPARROW:
            self.menu.move_focus(-1)
        elif ord(key) == 27:
            self.menu.end_menu()
            return

        self.presenter.display_menu(self.menu)

    def on_exit(self, context: IGameContext) -> None:
        pass
