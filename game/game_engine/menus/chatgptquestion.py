from typing import Any, Dict, List
from game.game_engine.action import Action
from abc import ABC, abstractmethod


class IMenu(ABC):
    """
    Interface for a menu system that defines the required methods for managing
    actions, attributes, and focus within a menu. Classes implementing this 
    interface should provide concrete implementations for each method to handle 
    various menu functionalities such as setting actions, moving focus, and 
    ending the menu.

    Methods
    -------
    get_attr(attr_id: str) -> Any:
        Retrieve a specific attribute from the menu by its identifier.
    
    get_actions_ids() -> List[str]:
        Return a list of all action identifiers registered in the menu.
    
    get_focus() -> int:
        Return the current focus position in the menu.
    
    set_action(action: Action, action_id: str) -> None:
        Register a new action with the given identifier or update an existing 
        action in the menu.
    
    unregister_action(action_id: str) -> None:
        Unregister an action from the menu by its identifier.
    
    move_focus(direction: int) -> None:
        Change the focus within the menu by moving it in the specified direction.
    
    call_action_on_focus() -> None:
        Invoke the action associated with the currently focused menu item.
    
    end_menu() -> None:
        End the menu, typically by invoking a 'back' or 'exit' action.
    """

    def __init__(self) -> None:
        super().__init__()
      
    @abstractmethod
    def get_attr(self, attr_id: str) -> Any:
        pass  
    
    @abstractmethod
    def get_actions_ids(self) -> List[str]:
        pass
    
    @abstractmethod
    def get_focus(self) -> int:
        pass
    
    @abstractmethod
    def set_action(
        self, action: Action, action_id: str
    ) -> None:
        pass

    @abstractmethod
    def unregister_action(self, action_id: str) -> None:
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

class BaseMenu(IMenu):
    def __init__(self, attrs: Dict[str, Any] = {}) -> None:
        super().__init__()
        self.actions_ids: List[str] = []
        self.actions: Dict[str, Action] = {}
        self.focus: int = 0
        self.attrs: Dict[str, Any] = attrs

    def get_actions_ids(self) -> List[str]:
        return self.actions_ids
    
    def get_attr(self, attr_id: str) -> Any:
        return self.attrs[attr_id]
    
    def get_focus(self) -> int:
        return self.focus

    def set_action(self, action: Action, action_id: str) -> None:
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
