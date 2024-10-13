from abc import ABC, abstractmethod
from typing import Optional, Tuple
from game.game_engine.menus.menu import IMenu

class IMenuPresenter(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def display_menu(self, menu: Optional[IMenu] = None) -> None:
        pass

    @abstractmethod
    def message(self, message: str, pos: Tuple[int, int]) -> None:
        pass
    @abstractmethod
    def clear_menu(self) -> None:
        pass
