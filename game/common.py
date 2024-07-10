from enum import Enum


from enum import Enum

class ComparableEnum(Enum):
    def __lt__(self, other):
        if isinstance(other, (int, ComparableEnum)):
            return self.value < (other.value if isinstance(other, ComparableEnum) else other)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, (int, ComparableEnum)):
            return self.value <= (other.value if isinstance(other, ComparableEnum) else other)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, (int, ComparableEnum)):
            return self.value > (other.value if isinstance(other, ComparableEnum) else other)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, (int, ComparableEnum)):
            return self.value >= (other.value if isinstance(other, ComparableEnum) else other)
        return NotImplemented

class Hint(ComparableEnum):
    NUMBER_OF_LETTERS = 3
    RIGHT_POS = 2
    WRONG_POS = 1
    WRONG_LETTER = 0
    MAX_LETTERS = 4
    UNKOWN_LETTER = -1

# Define constants based on the enum values
NUMBER_OF_LETTERS = Hint.NUMBER_OF_LETTERS
RIGHT_POS = Hint.RIGHT_POS
WRONG_POS = Hint.WRONG_POS
WRONG_LETTER = Hint.WRONG_LETTER
MAX_LETTERS = Hint.MAX_LETTERS
UNKOWN_LETTER = Hint.UNKOWN_LETTER

class Attempt:
    def __init__(self, guess: str, correct_word: str) -> None:
        self.guess: str = guess
        self.feedbacks: list[int] = self.apply_feedback(guess, correct_word)

    def apply_feedback(self, guess: str, correct_word: str) -> list[int]:
        feedbacks = [WRONG_LETTER for _ in guess]
        feedbacks = self.mark_position_hints(guess, correct_word, feedbacks)
        feedbacks = self.unmark_excess_wrong_pos(guess, correct_word, feedbacks)
        return feedbacks

    def mark_position_hints(self, guess: str, correct_word: str, feedbacks: list[int]) -> list[int]:
        for pos, letter in enumerate(guess):
            if letter == correct_word[pos]:
                feedbacks[pos] = RIGHT_POS
            elif letter in correct_word:
                feedbacks[pos] = WRONG_POS
        return feedbacks

    def unmark_excess_wrong_pos(self, guess: str, correct_word: str, feedbacks: list[int]) -> list[int]:
        for letter in set(guess):
            letter_indexes = [i for i, l in enumerate(guess) if l == letter]
            wrong_pos_indexes = [i for i in letter_indexes if feedbacks[i] == WRONG_POS]
            
            right_pos_hints = sum(feedbacks[i] == RIGHT_POS for i in letter_indexes)
            max_wrong_pos_hints = correct_word.count(letter) - right_pos_hints
            
            for count, i in enumerate(wrong_pos_indexes):
                if count > max_wrong_pos_hints:
                    feedbacks[i] = WRONG_LETTER
        return feedbacks

    def __iter__(self):
        for i, letter in enumerate(self.guess):
            feedback = self.feedbacks[i]
            yield letter, feedback, i