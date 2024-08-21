###########################################################################
################                                       ####################
################                 MATCH                 ####################
################                                       ####################
###########################################################################


from abc import ABC
from typing import List

import unidecode

from game.game_states.end_match_menu import MatchResult
from game.model.challenge import IChallenge
from game.model.imatch import IMatch
from game.viewer.terminal_manipulator import IDisplayCore


class Match(IMatch):
    def __init__(self, challenges: List[IChallenge], accepted_words: List[str]) -> None:

        self.challenges: List[IChallenge] = challenges
        self.accepted_words = accepted_words

        self.input_buffer: str = [" " for i in range(5)]
        self.cursor = 0

        self.lim_guesses: int = 5 + len(challenges)
        self.n_attempts: int = 0
        self._won: int = 0

    def won_the_game(self):
        for challenge in self.challenges:
            if not challenge.solved:
                return 0
        return 1

    def get_words(self) -> List[str]:
        return [challenge.get_word() for challenge in self.challenges]

    def get_n_attempts(self) -> int:
        return self.n_attempts

    def get_challenges(self) -> List[IChallenge]:
        return self.challenges

    def move_cursor_right(self) -> None:
        if self.cursor < 5:
            self.cursor += 1

    def delete_letter(self, pos: int) -> None:
        if 0 <= pos <= 4:
            self.input_buffer[pos] = " "
        if pos != self.cursor:
            self.move_cursor_left()

    def move_cursor_left(self) -> None:
        if self.cursor > 0:
            self.cursor -= 1

    def check_valid_word(self, word: str) -> bool:
        return word.lower() in self.accepted_words

    def input_letter(self, letter) -> str:
        if self.cursor < 5:
            self.input_buffer[self.cursor] = letter
            self.move_cursor_right()
            return letter
        return ""

    def submit_guess(self) -> str:
        if any([x == " " for x in self.input_buffer]):
            return ""
        guess = "".join(self.input_buffer)
        self.input_buffer = [" " for i in range(5)]
        self.cursor = 0
        return guess

    def won(self) -> bool:
        return self._won

    def get_results(self):

        return MatchResult(self.won(), self.get_n_attempts(), self.get_words())

    def update(self, guess: str):

        # GANHOU

        # CORRIGE
        for i in range(len(self.challenges)):
            if not self.challenges[i].solved:
                self.challenges[i].update(unidecode.unidecode(guess))

        self.n_attempts += 1
        if self.won_the_game():
            self._won = 1
            return 1
        # PERDEU
        if self.n_attempts == self.lim_guesses:
            return 1
        return 0
