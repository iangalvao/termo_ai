from abc import ABC, abstractmethod


class GameState(ABC):
    @abstractmethod
    def on_enter(self, **kwargs):
        pass

class PlayingState(GameState):
    def on_enter(self, level: int = 1, score: int = 0, **kwargs):
        print(f"Entering level {level} with score {score}")

state = PlayingState()
state.on_enter(level=2, score=100)
