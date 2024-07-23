from enum import Enum


from enum import Enum


class ComparableEnum(Enum):
    def __lt__(self, other):
        if isinstance(other, (int, ComparableEnum)):
            return self.value < (
                other.value if isinstance(other, ComparableEnum) else other
            )
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, (int, ComparableEnum)):
            return self.value <= (
                other.value if isinstance(other, ComparableEnum) else other
            )
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, (int, ComparableEnum)):
            return self.value > (
                other.value if isinstance(other, ComparableEnum) else other
            )
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, (int, ComparableEnum)):
            return self.value >= (
                other.value if isinstance(other, ComparableEnum) else other
            )
        return NotImplemented


class Hint(ComparableEnum):
    NUMBER_OF_LETTERS = 3
    RIGHT_POS = 2
    WRONG_POS = 1
    WRONG_LETTER = 0
    MAX_LETTERS = 4
    UNKNOWN_LETTER = -1


# Define constants based on the enum values
NUMBER_OF_LETTERS = Hint.NUMBER_OF_LETTERS
RIGHT_POS = Hint.RIGHT_POS
WRONG_POS = Hint.WRONG_POS
WRONG_LETTER = Hint.WRONG_LETTER
MAX_LETTERS = Hint.MAX_LETTERS
UNKNOWN_LETTER = Hint.UNKNOWN_LETTER
