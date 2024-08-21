from argparse import Action
from typing import Any, Dict, List
from game.game_states.menu import IMenu


class BaseMenu(IMenu):
    def __init__(self) -> None:
        super().__init__()
        self.actions_ids: List[str] = []
        self.actions: Dict[str, Action] = {}
        self.focus: int = 0

    def set_action(self, action: Action, action_id: int):
        if not action_id or not isinstance(action_id, str):
            raise ValueError("Action ID must be a non-empty string.")

        if action_id not in self.actions.keys():
            self.actions_ids.append(action_id)
        self.actions[action_id] = action

    def unregister_action(self, action_id: str) -> None:
        if action_id not in self.actions:
            raise KeyError(f"Action ID '{action_id}' not found.")
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
            s += k + ": " + str(v) + ";\n "
        s += "Actions_ids:\n"
        for action_id in self.actions_ids:
            s += action_id + "; "
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
