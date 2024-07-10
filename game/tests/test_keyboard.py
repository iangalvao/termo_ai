import pytest
from game.common import Hint
from game.keyboard import Keyboard

# Mock class for IAttempt
class MockAttempt:
    def __init__(self, guess, correct_word):
        self.guess = guess
        self.correct_word = correct_word

    def __iter__(self):
        return iter([
            ('A', Hint.RIGHT_POS),
            ('B', Hint.WRONG_POS),
            ('C', Hint.WRONG_LETTER),
            ('D', Hint.UNKNOWN_LETTER),
        ])

# Test for process_hints
def test_process_hints():
    keyboard = Keyboard()
    attempt = MockAttempt("ABCD", "WXYZ")

    # Process hints
    keyboard.process_hints(attempt)

    # Verify the state of the keyboard
    assert keyboard.get_letter_hint('A') == Hint.RIGHT_POS
    assert keyboard.get_letter_hint('B') == Hint.WRONG_POS
    assert keyboard.get_letter_hint('C') == Hint.WRONG_LETTER
    assert keyboard.get_letter_hint('D') == Hint.UNKNOWN_LETTER
    assert keyboard.get_letter_hint('E') == Hint.UNKNOWN_LETTER

    # Check other keys are still at UNKNOWN_LETTER state
    for key in "FGHIJKLMNOPQRSTUVWXYZ":
        assert keyboard.get_letter_hint(key) == Hint.UNKNOWN_LETTER

if __name__ == "__main__":
    pytest.main()
