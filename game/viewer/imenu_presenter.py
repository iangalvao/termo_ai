from abc import ABC, abstractmethod

from game.game_states.menu import IMenu


class IMenuPresenter(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def display_menu(self, menu: IMenu) -> None:
        pass

    @abstractmethod
    def clear_menu(self) -> None:
        pass
