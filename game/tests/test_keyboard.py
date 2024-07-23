import pytest
from game.model.hint import Hint
from game.model.keyboard import Keyboard


# Mock class for IAttempt
class MockAttempt:
    def __init__(self, guess, correct_word):
        self.guess = guess
        self.correct_word = correct_word

    def __iter__(self):
        return iter(
            [
                ("A", Hint.RIGHT_POS, 0),
                ("B", Hint.WRONG_POS, 1),
                ("C", Hint.WRONG_LETTER, 2),
                ("D", Hint.UNKNOWN_LETTER, 3),
            ]
        )


# Test for process_hints
def test_process_hints():
    keyboard = Keyboard()
    attempt = MockAttempt("ABCD", "WXYZ")

    # Process hints
    keyboard.process_hints(attempt)

    # Verify the state of the keyboard
    assert keyboard.get_letter_hint("A") == Hint.RIGHT_POS
    assert keyboard.get_letter_hint("B") == Hint.WRONG_POS
    assert keyboard.get_letter_hint("C") == Hint.WRONG_LETTER
    assert keyboard.get_letter_hint("D") == Hint.UNKNOWN_LETTER
    assert keyboard.get_letter_hint("E") == Hint.UNKNOWN_LETTER

    # Check other keys are still at UNKNOWN_LETTER state
    for key in "FGHIJKLMNOPQRSTUVWXYZ":
        assert keyboard.get_letter_hint(key) == Hint.UNKNOWN_LETTER


def test_iter_empty_keyboard():
    keys = "QWERTYUIOPASDFGHJKLZXCVBNM"
    i = 0
    j = 0
    keyboard = Keyboard()
    for keyline, n in keyboard:
        assert n == i
        for key, hint in keyline:
            assert hint == Hint.UNKNOWN_LETTER
            assert key == keys[j]
            j += 1
        i += 1


if __name__ == "__main__":
    pytest.main()
