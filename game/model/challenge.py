###########################################################################
################                  DESAFIO              ####################
###########################################################################


from abc import ABC
import unidecode
from game.model.attempt import Attempt
from game.model.keyboard import Keyboard


class IChallenge(ABC):
    def __init__(self) -> None:
        super().__init__()

    def get_lim_guesses(self) -> int:
        pass

    def get_attempts(self) -> list[Attempt]:
        pass

    def get_keyboard(self) -> Keyboard:
        pass

    def get_word(self) -> str:
        pass

    def update(self) -> Attempt:
        pass


class Challenge:
    def __init__(self, palavra, lim_guesses=6) -> None:
        self.chutes = []
        self.feedbacks = []
        self.attempts: List[Attempt] = []
        self.teclado = Keyboard()
        self.palavra = palavra
        self.solved = 0
        self.lim_guesses = 6

    def get_lim_guesses(self):
        return self.lim_guesses

    def get_keyboard(self):
        return self.teclado

    def get_attempts(self):
        return self.attempts

    def get_word(self):
        return self.palavra

    def update(self, chute):
        if chute == self.palavra:
            self.solved = 1
        attempt = Attempt(chute, self.palavra)
        self.attempts.append(attempt)

        self.teclado.process_hints(attempt)
        # self.teclado.process_hints(chute, chute_corrigido)
        return attempt
