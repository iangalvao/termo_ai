from abc import ABC, abstractmethod
from typing import Callable


class IMenu(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def set_action(
        self, action: Callable[[], None], button_id: str, action_id: str
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
