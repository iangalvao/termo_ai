from abc import ABC
from typing import List

from game.model.challenge import IChallenge


class IMatch(ABC):
    def __init__(self, challenges: List[IChallenge], accepted_words: List[str]) -> None:
        super().__init__()

    def won(self) -> bool:
        pass

    def get_n_attempts(self) -> int:
        pass

    def get_challenges(self) -> List[IChallenge]:
        pass

    def get_words(self) -> List[str]:
        pass

    def delete_letter(self, pos: int) -> None:
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
