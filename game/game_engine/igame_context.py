from abc import ABC, abstractmethod


class IGameContext(ABC):
    @abstractmethod
    def change_state(self, state_id: str, **kwargs) -> None:
        pass

    @abstractmethod
    def handle_input(self, input) -> None:
        pass
