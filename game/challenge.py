###########################################################################
################                  DESAFIO              ####################
###########################################################################


import unidecode
from game.attempt import Attempt
from game.keyboard import Keyboard


class Challenge:
    def __init__(self, palavra, lim_guesses=6) -> None:
        self.chutes = []
        self.feedbacks = []
        self.attempts: list[Attempt] = []
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

    def update(self, chute):
        if chute == self.palavra:
            self.solved = 1
        attempt = Attempt(chute, self.palavra)
        self.attempts.append(attempt)

        self.teclado.process_hints(attempt)
        # self.teclado.process_hints(chute, chute_corrigido)
        return attempt
