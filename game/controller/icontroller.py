from abc import ABC


class IController(ABC):
    def __init__(self) -> None:
        super().__init__()

    def process_input(self, key: str) -> None:
        pass
