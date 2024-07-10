from typing import Tuple
import pytest
from game.terminal_presenter import TerminalPresenter,IPresenter


# Define a pytest fixture for the presenter
@pytest.fixture
def presenter():
    return TerminalPresenter()

# Test for go_to_line method
def test_go_to_line_positive(presenter):
    assert presenter.go_to_line(5) == "\033[5B", "Should move down 5 lines"

def test_go_to_line_negative(presenter):
    assert presenter.go_to_line(-3) == "\033[3A", "Should move up 3 lines"

def test_go_to_line_zero(presenter):
    assert presenter.go_to_line(0) == "", "Should not move the cursor"

# Test for go_to_char method
def test_go_to_char_positive(presenter):
    assert presenter.go_to_char(4) == "\033[4C", "Should move right 4 characters"

def test_go_to_char_negative(presenter):
    assert presenter.go_to_char(-2) == "\033[2D", "Should move left 2 characters"

def test_go_to_char_zero(presenter):
    assert presenter.go_to_char(0) == "", "Should not move the cursor"

# Test for go_to_pos method
def test_go_to_pos_origin(presenter):
    assert presenter.go_to_pos((0, 0)) == "", "Should not move the cursor"

def test_go_to_pos_positive(presenter):
    assert presenter.go_to_pos((3, 5)) == "\033[3B\033[5C", "Should move down 3 lines and right 5 characters"

def test_go_to_pos_negative(presenter):
    assert presenter.go_to_pos((-2, -4)) == "\033[2A\033[4D", "Should move up 2 lines and left 4 characters"

def test_go_to_pos_mixed(presenter):
    assert presenter.go_to_pos((2, -3)) == "\033[2B\033[3D", "Should move down 2 lines and left 3 characters"

# Test for string_size method
def test_string_size_no_escapes(presenter):
    assert presenter.string_size("Hello, World!") == 13, "Should return the length of the string without escape sequences"

def test_string_size_with_escapes(presenter):
    assert presenter.string_size("\033[1mBold Text\033[0m") == 9, "Should return the length of the visible characters, ignoring escape sequences"

def test_string_size_empty(presenter):
    assert presenter.string_size("") == 0, "Should return 0 for an empty string"

def test_string_size_only_escapes(presenter):
    assert presenter.string_size("\033[32m\033[1mImportant\033[0m") == 9, "Should return 0 since there are no visible characters"

def test_string_size_punctuation(presenter):
    assert presenter.string_size("Hello, World!") == 13, "Should correctly count punctuation marks as part of the string length"

def test_string_size_numbers_and_punctuation(presenter):
    assert presenter.string_size("1234!@#$%^&*()_+") == 16, "Should correctly count numbers and punctuation marks"


def test_string_at_pos_basic(presenter):
    result = presenter.string_at_pos("Hello", (3, 5))
    expected = "\033[3B\033[5CHello\033[3A\033[10D"
    assert result == expected, f"Expected: {expected}, but got: {result}"

def test_string_at_pos_empty_string(presenter):
    result = presenter.string_at_pos("", (0, 0))
    expected = ""
    assert result == expected, f"Expected: {expected}, but got: {result}"

def test_string_at_pos_long_string(presenter):
    result = presenter.string_at_pos("This is a long string", (1, 10))
    expected = "\033[1B\033[10CThis is a long string\033[1A\033[31D"
    assert result == expected#, #f"Expected: {expected}, but got: {result}"

def test_string_at_pos_unicode_characters(presenter):
    result = presenter.string_at_pos("Unicode: 😊🚀", (2, 3))
    expected = "\033[2B\033[3CUnicode: 😊🚀\033[2A\033[14D"
    assert result == expected#, #f"Expected: {expected}, but got: {result}"
    
def test_clean_line_at_pos_basic():
    presenter = TerminalPresenter(line_length=75)
    result = presenter.clean_line_at_pos(1)
    expected = "\033[1B" + " " * 75 + "\033[1A\033[75D"
    assert result == expected
    
def test_clean_line_at_pos_custom_length():
    presenter = TerminalPresenter(line_length=50)
    result = presenter.clean_line_at_pos(7)
    expected = "\033[7B" + " " * 50 + "\033[7A\033[50D"
    assert result == expected
    
def test_clean_line_at_pos_zero_length():
    presenter = TerminalPresenter(line_length=0)
    result = presenter.clean_line_at_pos(1)
    expected = "\033[1B\033[1A"
    assert result == expected

if __name__ == "__main__":
    pytest.main()
