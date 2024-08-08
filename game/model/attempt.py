from typing import Iterator, Tuple
from game.model.hint import *
from abc import ABC


class IAttempt(ABC):
    def __init__(self, guess: str, correct_word: str) -> None:
        super().__init__()

    def get_feedbacks(self) -> list[Hint]:
        pass

    def get_guess(self) -> str:
        pass

    def __iter__(self) -> Iterator[Tuple[str, str, int]]:
        pass



class Attempt(IAttempt):
    def __init__(self, guess: str, correct_word: str = None) -> None:
        self.guess: str = guess
        self.feedbacks: list[Hint] = self.apply_feedback(guess, correct_word)

    def get_feedbacks(self) -> list[Hint]:
        return self.feedbacks

    def get_guess(self) -> str:
        return self.guess

    def apply_feedback(self, guess: str, correct_word: str) -> list[Hint]:
        feedbacks = [WRONG_LETTER for _ in guess]
        feedbacks = self.mark_position_hints(guess, correct_word, feedbacks)
        feedbacks = self.unmark_excess_wrong_pos(guess, correct_word, feedbacks)
        return feedbacks

    def mark_position_hints(
        self, guess: str, correct_word: str, feedbacks: list[int]
    ) -> list[Hint]:
        for pos, letter in enumerate(guess):
            if letter == correct_word[pos]:
                feedbacks[pos] = RIGHT_POS
            elif letter in correct_word:
                feedbacks[pos] = WRONG_POS
        return feedbacks

    def unmark_excess_wrong_pos(
        self, guess: str, correct_word: str, feedbacks: list[int]
    ) -> list[Hint]:
        for letter in set(guess):
            letter_indexes = [i for i, l in enumerate(guess) if l == letter]
            wrong_pos_indexes = [i for i in letter_indexes if feedbacks[i] == WRONG_POS]

            right_pos_hints = sum(feedbacks[i] == RIGHT_POS for i in letter_indexes)
            max_wrong_pos_hints = correct_word.count(letter) - right_pos_hints

            for count, i in enumerate(wrong_pos_indexes):
                if count >= max_wrong_pos_hints:
                    feedbacks[i] = WRONG_LETTER
        return feedbacks

    def __iter__(self) -> Iterator[Tuple[str, str, int]]:
        for i, letter in enumerate(self.guess):
            feedback = self.feedbacks[i]
            yield letter, feedback, i

