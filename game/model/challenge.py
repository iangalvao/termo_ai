###########################################################################
################                  DESAFIO              ####################
###########################################################################


from abc import ABC, abstractmethod
from typing import List
from game.model.attempt import Attempt
from game.model.keyboard import Keyboard


class IChallenge(ABC):
    def __init__(self) -> None:
        super().__init__()
    @abstractmethod
    def get_lim_guesses(self) -> int:
        pass
    @abstractmethod
    def get_attempts(self) -> list[Attempt]:
        pass
    @abstractmethod
    def get_keyboard(self) -> Keyboard:
        pass
    @abstractmethod
    def get_word(self) -> str:
        pass
    @abstractmethod
    def update(self, guess:str) -> Attempt:
        pass
    @abstractmethod
    def is_solved(self) -> bool:
        pass
    

class Challenge(IChallenge):

    def __init__(self, palavra, lim_guesses=6) -> None:
        self.attempts: List[Attempt] = []
        self.teclado = Keyboard()
        self.palavra = palavra
        self.solved = False
        self.lim_guesses = 6

    def get_lim_guesses(self) -> int:
        return self.lim_guesses

    def get_keyboard(self) -> Keyboard:
        return self.teclado

    def get_attempts(self) -> List[Attempt]:
        return self.attempts

    def get_word(self) -> str:
        return self.palavra

    def update(self, chute: str) -> Attempt:
        if chute == self.palavra:
            self.solved = True
        attempt = Attempt(chute, self.palavra)
        self.attempts.append(attempt)

        self.teclado.process_hints(attempt)
        # self.teclado.process_hints(chute, chute_corrigido)
        return attempt
    def is_solved(self) -> bool:
        return self.solved