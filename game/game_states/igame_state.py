from abc import ABC, abstractmethod

from game.game_states.igame_context import IGameContext


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
