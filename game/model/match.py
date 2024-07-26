###########################################################################
################                                       ####################
################                 MATCH                 ####################
################                                       ####################
###########################################################################


from abc import ABC
from typing import List

import unidecode

from game.model.challenge import IChallenge
from game.viewer.terminal_manipulator import IDisplayCore


class IMatch(ABC):
    def __init__(self, tmanipulator: IDisplayCore) -> None:
        super().__init__()

    def update(self, guess: str) -> None:
        pass

    def submit_guess(self) -> str:
        pass


class Match(IMatch):
    def __init__(
        self,
        challenges: List[IChallenge],
    ) -> None:

        self.challenges: List[IChallenge] = challenges
        self.input_buffer: str = " " * 5
        self.lim_guesses: int = 5 + len(challenges)
        self.n_attempts: int = 0
        self._won: int = 0
        self.cursor = 0

    def won_the_game(self):
        for challenge in self.challenges:
            if not challenge.solved:
                return 0
        return 1

    def increment_cursor(self) -> None:
        if self.cursor < 4:
            self.cursor += 1

    def check_valid_word(self, word: str) -> bool:
        return word.lower() in self.accepted_words.keys()

    def input_letter(self, letter):
        self.input_buffer[self.cursor] = letter
        self.increment_cursor()

    def submit_guess(self) -> str:
        if any([lambda x: x == " " for x in self.input_buffer]):
            return ""
        else:
            guess = self.input_buffer
            self.input_buffer = " " * 5
            self.cursor = 0
            return guess

    def won(self) -> bool:
        return self._won

    def update(self, guess: str):

        # GANHOU

        # CORRIGE
        for i in range(len(self.challenges)):
            if not self.challenges[i].solved:
                self.challenges[i].update(unidecode(guess))

        if self.won_the_game(self.challenges):
            self._won = 1
            return 1
        # PERDEU
        if self.n_attempts == self.lim_chutes:
            return 1
        self.n_attempts += 1
        return 0
