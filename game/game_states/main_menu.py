from game.game_states.action import Action
from game.game_states.base_menu import BaseMenu
from game.game_states.igame_context import IGameContext
from game.game_states.menustate import MenuState
from game.viewer.imenu_presenter import IMenuPresenter


class MainMenu(BaseMenu):
    def __init__(self) -> None:
        super().__init__()

    def end_menu(self) -> None:
        # No return function on main menu. Override to quit instead.
        self.actions["quit"]()


# This completes the implementation of menustate, by implementing the method on enter.
# This is the point where the menu is in fact created, and should be implemented on
# every menu state.
class MainMenuState(MenuState):

    def __init__(self, presenter: IMenuPresenter) -> None:
        super().__init__(presenter)

    def on_enter(self, context: IGameContext) -> None:
        self.menu = MainMenu()

        self.menu.set_action(
            Action(
                context.change_state,
                state_id="play_state",
                n_challenges=1,
            ),
            "quick match",
        )
        self.menu.set_action(
            Action(context.change_state, state_id="match_config"), "new match"
        )
        self.menu.set_action(
            Action(
                context.change_state,
                state_id="quit_state",
                previous_state="main_menu_state",
            ),
            "quit",
        )
        self.presenter.display_menu(self.menu)
