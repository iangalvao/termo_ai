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

    def won(self) -> bool:
        pass

    def get_n_attempts(self) -> int:
        pass

    def get_challenges(self) -> List[IChallenge]:
        pass

    def get_words(self) -> List[str]:
        pass

    def input_letter(self) -> str:
        pass

    def move_cursor_left(self) -> None:
        pass

    def move_cursor_right(self) -> None:
        pass

    def submit_guess(self) -> str:
        pass

    def check_valid_word(self, word: str) -> bool:
        pass

    def update(self, guess: str) -> None:
        pass


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
        if self.cursor < 4:
            self.cursor += 1

    def move_cursor_left(self) -> None:
        if self.cursor > 0:
            self.cursor -= 1

    def check_valid_word(self, word: str) -> bool:
        return word.lower() in self.accepted_words.keys()

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
