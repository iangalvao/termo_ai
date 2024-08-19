from argparse import Action
from dataclasses import dataclass
from typing import Any, List

from game.game_states.base_menu import BaseMenu
from game.game_states.igame_context import IGameContext
from game.game_states.menustate import MenuState
from game.model.match import IMatch
from game.viewer.imenu_presenter import IMenuPresenter


@dataclass
class MatchResult:
    won: bool
    n_attempts: int
    correct_words: List[str]


class EndMatchMenu(BaseMenu):
    def __init__(self, result: MatchResult) -> None:
        super().__init__()
        self.results = result

    def get_results(self):
        return self.results

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EndMatchMenu):
            return super().__eq__(other) and self.results == other.results
        return False

    def __str__(self) -> str:
        return super().__str__() + f" Results:\n{self.results}"

    def __repr__(self) -> str:
        return str(self)


# Other implementation of menu state. This one receives a extra argument to create the menu,
# that is the results being displayed.
class EndMatchState(MenuState):
    def __init__(self, presenter: IMenuPresenter) -> None:
        super().__init__(presenter=presenter)

    def on_enter(self, context: IGameContext, match: IMatch) -> None:
        results = match.get_results()
        self.menu = EndMatchMenu(results)

        self.menu.set_action(
            Action(
                context.change_state,
                **{"state_id": "play_state", "n_challenges": match.n_challenges},
            ),
            "retry",
        )
        self.menu.set_action(
            Action(context.change_state, **{"state_id": "main_menu_state"}), "main menu"
        )
        self.menu.set_action(
            Action(context.change_state, **{"state_id": "quit_state"}), "quit"
        )
        self.menu.set_action(
            Action(context.change_state, **{"state_id": "play_state"}), "back"
        )
        self.presenter.display_menu(self.menu)
