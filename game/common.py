from enum import Enum


class Hint(Enum):
    NUMBER_OF_LETTERS = 3
    RIGHT_POS = 2
    WRONG_POS = 1
    WRONG_LETTER = 0
