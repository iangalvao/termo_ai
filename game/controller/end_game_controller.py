from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List
from game.controller.controllercore import DOWNARROW, UPARROW
from dataclasses import dataclass


class IGameContext(ABC):
    @abstractmethod
    def change_state(self, state_id: str, **kwargs) -> None:
        pass

    @abstractmethod
    def handle_input(self, input) -> None:
        pass


class IMenu(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def set_action(
        self, action: Callable[[], None], button_id: str, action_id: str
    ) -> None:
        pass

    @abstractmethod
    def remove_action_hook(self, action_id: str) -> None:
        pass

    @abstractmethod
    def move_focus(self, direction: int) -> None:
        pass

    @abstractmethod
    def call_action_on_focus(self) -> None:
        pass

    @abstractmethod
    def end_menu(self) -> None:
        pass


class IMenuPresenter(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def display_menu(self, menu: IMenu) -> None:
        pass

    @abstractmethod
    def clear_menu(self) -> None:
        pass


class IGameState(ABC):
    @abstractmethod
    def handle_input(self, context: IGameContext, input: str) -> None:
        pass

    @abstractmethod
    def on_enter(self, context) -> None:
        pass

    @abstractmethod
    def on_exit(self, context) -> None:
        pass


# This class does not implement on_enter abstract method. Thus, is a incomplete implementation,
# intended to be used only as a base for other menu states
class MenuState(IGameState):
    def __init__(self, presenter: IMenuPresenter) -> None:
        super().__init__()
        self.menu: IMenu = None
        self.presenter: IMenuPresenter = presenter

    def handle_input(self, context: IGameContext, key: str) -> None:
        if ord(key) == 10:
            self.menu.call_action_on_focus()
        elif key == DOWNARROW:
            self.menu.move_focus(1)
        elif key == UPARROW:
            self.menu.move_focus(-1)
        elif ord(key) == 27:
            self.menu.end_menu()

        self.presenter.display_menu(self.menu)

    def on_exit(self, context: IGameContext) -> None:
        self.presenter.clear_menu()


class BaseMenu(IMenu):
    def __init__(self) -> None:
        super().__init__()
        self.actions_ids: List[str] = []
        self.actions: Dict[str, Action] = {}
        self.focus: int = 0

    def set_action(self, action: Callable[[], None], action_id: int):
        if action_id in self.actions.keys():
            # OVERRIDE
            self.actions = action
        else:
            self.actions_ids.append(action_id)
            self.actions[action_id] = action

    def remove_action_hook(self, action_id: str) -> None:
        self.actions.pop(action_id)
        self.actions_ids.remove(action_id)

    def move_focus(self, direction: int) -> None:
        if 0 <= self.focus + direction < len(self.actions_ids):
            self.focus += direction

    def call_action_on_focus(self) -> None:
        self.actions[self.actions_ids[self.focus]]()

    def end_menu(self) -> None:
        self.actions["back"]()

    def __str__(self):
        s = ""
        s += "Actions dict:\n"
        for k, v in self.actions.items():
            s += k + ": " + str(v) + "; "
        s += "Actions_ids:\n"
        for action_id in self.actions_ids:
            s += action_id + ";"
        return s

    def __repr__(self):
        return str(self)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BaseMenu):
            return (
                self.actions_ids == other.actions_ids
                and self.actions == other.actions
                and self.focus == other.focus
            )
        return False


class MainMenu(BaseMenu):
    def __init__(self) -> None:
        super().__init__()

    def end_menu(self) -> None:
        # No return function on main menu. Override to quit instead.
        self.actions["quit"]()


@dataclass
class MatchResult:
    won: bool
    n_attempts: int
    correct_words: List[str]


class Action:
    def __init__(self, f: Callable[[], None], **kwargs) -> None:
        self.func = f
        self.fixed_args = kwargs

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        combined_args = {**self.fixed_args, **kwds}
        return self.func(*args, **combined_args)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Action):
            return self.func == other.func and self.fixed_args == other.fixed_args
        return False

    def __str__(self) -> str:
        return f"Action(func={self.func.__name__}, fixed_args={self.fixed_args})"

    def __repr__(self) -> str:
        return str(self)


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
                **{"state_id": "play_state", "n_challenges": 1},
            ),
            "quick match",
        )
        self.menu.set_action(
            Action(context.change_state, **{"state_id": "match_config"}), "new match"
        )

        self.menu.set_action(
            Action(context.change_state, **{"state_id": "quit_state"}), "quit"
        )
        self.presenter.display_menu(self.menu)


class EndMatchMenu(BaseMenu):
    def __init__(self, result: MatchResult) -> None:
        super().__init__()
        self.results = result

    def get_results(self):
        return self.results

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EndMatchMenu):
            return super().__eq__(self, other) and self.results == other.results
        return False

    def __str__(self) -> str:
        return super().__str__() + f" Results:{self.results}"

    def __repr__(self) -> str:
        return str(self)


# Other implementation of menu state. This one receives a extra argument to create the menu,
# that is the results being displayed.
class EndMatchState(MenuState):
    def __init__(self, presenter: IMenuPresenter) -> None:
        super().__init__(presenter=presenter)

    def on_enter(self, context: IGameContext, match) -> None:
        self.menu = EndMatchMenu(match.won, match.n_attempts, match.words)

        self.menu.set_action(
            Action(
                context.change_state,
                {"state_id": "play_state", "n_challenges": match.n_challenges},
            ),
            "retry",
        )
        self.menu.set_action(
            Action(context.change_state, {"state_id": "main_menu_state"}), "main menu"
        )
        self.menu.set_action(
            Action(context.change_state, {"state_id": "quit_state"}), "quit"
        )
        self.menu.set_action(
            Action(context.change_state, {"state_id": "play_state"}), "back"
        )
        self.presenter.display_menu(self.menu)


# Not yet implemented
class MatchConfigState(MenuState):
    def __init__(self) -> None:
        pass


# Not yet implemented
class PlayState(IGameState):
    def __init__(self) -> None:
        pass


class BaseMenuPresenter(IMenuPresenter):
    def __init__(self) -> None:
        super().__init__()

    def display_base_menu(self, menu: BaseMenu):
        for i, action_id in enumerate(menu.actions_ids):
            pos = (i, 0)
            # this go on printing every action at one line, and highlightning the one in focus.

    def display_menu(self, menu: IMenu) -> None:
        if isinstance(menu, BaseMenu):
            self.display_base_menu(menu)


class EndMatchMenuPresenter(BaseMenuPresenter):
    def __init__(self) -> None:
        super().__init__()

    def display_menu(self, menu: EndMatchMenu) -> None:
        results = EndMatchMenu.get_results()
        # Do something with result to print it...
        # something like:
        # self.display_results()
        # self.diplay_base_menu(menu)

    def clear_menu(self) -> None:
        # If there is a area specific for the menu, this should be implemented. Otherwise, not.
        pass
