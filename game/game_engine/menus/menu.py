from abc import ABC, abstractmethod
from typing import Any, List
from game.game_engine.action import Action


class IMenu(ABC):
    """
    Interface for a menu system that defines the required methods for managing
    actions, attributes, and focus within a menu.
    """

    @abstractmethod
    def get_attr(self, attr_id: str) -> Any:
        """
        Retrieve a specific attribute from the menu by its identifier.

        Parameters
        ----------
        attr_id : str
            The identifier of the attribute to retrieve.

        Returns
        -------
        Any
            The value of the attribute corresponding to the provided ID.
        """
        pass  

    @abstractmethod
    def get_actions_ids(self) -> List[str]:
        """
        Return a list of all action identifiers registered in the menu.

        Returns
        -------
        List[str]
            A list containing all registered action identifiers.
        """
        pass

    @abstractmethod
    def get_focus(self) -> int:
        """
        Return the current focus position in the menu.

        Returns
        -------
        int
            The index of the currently focused action.
        """
        pass
    
    @abstractmethod
    def set_action(self, action: Action, action_id: str) -> None:
        """
        Register a new action or update an existing one in the menu.

        Parameters
        ----------
        action : Action
            The action to be registered or updated.
        action_id : str
            The identifier for the action.

        Raises
        ------
        ValueError
            If the action_id is empty or not a string.
        """
        pass

    @abstractmethod
    def unregister_action(self, action_id: str) -> None:
        """
        Unregister an action from the menu by its identifier.

        Parameters
        ----------
        action_id : str
            The identifier of the action to be removed.

        Raises
        ------
        KeyError
            If the action_id does not exist in the menu.
        """
        pass

    @abstractmethod
    def move_focus(self, direction: int) -> None:
        """
        Change the focus within the menu.

        Parameters
        ----------
        direction : int
            The direction in which to move the focus. Positive values move the 
            focus forward, while negative values move it backward.
        """
        pass

    @abstractmethod
    def call_action_on_focus(self) -> None:
        """
        Invoke the action associated with the currently focused menu item.
        """
        pass

    @abstractmethod
    def end_menu(self) -> None:
        """
        End the menu, typically invoking a 'back' or 'exit' action.
        """
        pass

