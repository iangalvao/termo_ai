from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from game.game_engine.action import Action
from game.game_engine.menus.base_menu import BaseMenu
from game.game_engine.igame_context import IGameContext
from game.game_engine.game_states.menustate import MenuState
from game.game_engine.presenters.imenu_presenter import IMenuPresenter


@dataclass
class MatchResult:
    won: bool
    n_attempts: int
    correct_words: List[str]


class EndMatchMenu(BaseMenu):
    def __init__(self, attrs: Dict[str,Any]) -> None:
        super().__init__()
        self.results:MatchResult = attrs["result"]

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

    def on_enter(self, context: IGameContext, match_results: Optional[MatchResult] = None, **kwargs) -> None:
        if match_results:
            self.menu = EndMatchMenu({"results":match_results})

            self.menu.set_action(
                Action(
                    context.change_state,
                    {"state_id":"play_state",
                    "n_challenges":len(match_results.correct_words)},
                ),
                "retry",
            )
            self.menu.set_action(
                Action(context.change_state, {"state_id":"main_menu_state"}), "main menu"
            )
            self.menu.set_action(
                Action(
                    context.change_state,
                    {"state_id":"quit_state",
                    "previous_state":"end_match_state",
                    }
                ),
                "quit",
            )
            self.menu.set_action(
                Action(context.change_state, {"state_id":"play_state"}), "back"
            )
        self.presenter.display_menu(self.menu)
