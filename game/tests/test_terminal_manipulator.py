from typing import Tuple
import pytest
from game.terminal_manipulator import TerminalManipulator, ColoredString
from game.hint import *

from colorama import Back

COR_ERRADO = 0
COR_CERTO = 1
COR_POSICAO = 2
ENDC = 3


@pytest.fixture
def color_dict():
    return {
        COR_ERRADO: Back.LIGHTRED_EX,
        COR_CERTO: Back.GREEN,
        COR_POSICAO: Back.YELLOW,
        ENDC: Back.RESET,
    }


# Define a pytest fixture for the presenter
@pytest.fixture
def presenter(color_dict):
    return TerminalManipulator(color_dict)


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
    assert (
        presenter.go_to_pos((3, 5)) == "\033[3B\033[5C"
    ), "Should move down 3 lines and right 5 characters"


def test_go_to_pos_negative(presenter):
    assert (
        presenter.go_to_pos((-2, -4)) == "\033[2A\033[4D"
    ), "Should move up 2 lines and left 4 characters"


def test_go_to_pos_mixed(presenter):
    assert (
        presenter.go_to_pos((2, -3)) == "\033[2B\033[3D"
    ), "Should move down 2 lines and left 3 characters"


# Test for string_size method
def test_string_size_no_escapes(presenter):
    assert (
        presenter.string_size("Hello, World!") == 13
    ), "Should return the length of the string without escape sequences"


def test_string_size_with_escapes(presenter):
    assert (
        presenter.string_size("\033[1mBold Text\033[0m") == 9
    ), "Should return the length of the visible characters, ignoring escape sequences"


def test_string_size_empty(presenter):
    assert presenter.string_size("") == 0, "Should return 0 for an empty string"


def test_string_size_only_escapes(presenter):
    assert (
        presenter.string_size("\033[32m\033[1mImportant\033[0m") == 9
    ), "Should return 0 since there are no visible characters"


def test_string_size_punctuation(presenter):
    assert (
        presenter.string_size("Hello, World!") == 13
    ), "Should correctly count punctuation marks as part of the string length"


def test_string_size_numbers_and_punctuation(presenter):
    assert (
        presenter.string_size("1234!@#$%^&*()_+") == 16
    ), "Should correctly count numbers and punctuation marks"


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
    assert result == expected


def test_string_at_pos_unicode_characters(presenter):
    result = presenter.string_at_pos("Unicode: 😊🚀", (2, 3))
    expected = "\033[2B\033[3CUnicode: 😊🚀\033[2A\033[14D"
    assert result == expected


def test_clean_line_at_pos_basic(color_dict):
    presenter = TerminalManipulator(color_dict, line_length=75)
    result = presenter.clear_line_at_pos(1)
    expected = "\033[1B" + " " * 75 + "\033[1A\033[75D"
    assert result == expected


def test_clean_line_at_pos_custom_length(color_dict):
    presenter = TerminalManipulator(color_dict, line_length=50)
    result = presenter.clear_line_at_pos(7)
    expected = "\033[7B" + " " * 50 + "\033[7A\033[50D"
    assert result == expected


def test_clean_line_at_pos_zero_length(color_dict):
    presenter = TerminalManipulator(color_dict, line_length=0)
    result = presenter.clear_line_at_pos(1)
    expected = "\033[1B\033[1A"
    assert result == expected


@pytest.mark.parametrize(
    "string, expected",
    [("s", 1), ("á", 1), ("sapos", 5), ("     ", 5)],
)
def test_string_size_recebe_formatacao_de_posicionamento(string, expected, presenter):
    string = "\033[1C" + string
    tamanho = presenter.string_size(string)
    assert tamanho == expected


@pytest.mark.parametrize(
    "string, expected",
    [("s", 1), ("á", 1), ("sapos", 5), ("     ", 5)],
)
def test_string_size_recebe_sem_formatacao(string, expected, presenter):

    tamanho = presenter.string_size(string)
    assert tamanho == expected


@pytest.mark.parametrize(
    "cor, string, expected",
    [
        ("\033[93m", "s", 1),
        ("\033[93m", "á", 1),
        ("\033[93m", "sapos", 5),
        ("\033[93m", "     ", 5),
    ],
)
def test_string_size_recebe_formatacao_de_cor_com_duas_casas_numericas_apos_colchete(
    cor, string, expected, presenter
):
    string = cor + string
    tamanho = presenter.string_size(string)
    assert tamanho == expected


def test_string_size_recebe_linha_de_taclas_coloridas(presenter):
    s = "\033[94mQ\033[0m\033[94mW\033[0m"
    tamanho = presenter.string_size(s)
    assert tamanho == 2


@pytest.mark.parametrize(
    "cor, string, expected",
    [
        ("\033[101m", "s", 1),
        ("\033[101m", "á", 1),
        ("\033[101m", "sapos", 5),
        ("\033[101m", "     ", 5),
    ],
)
def test_string_size_recebe_formatacao_de_cor_com_tres_casas_numericas_apos_colchete(
    cor, string, expected, presenter
):
    string = cor + string
    tamanho = presenter.string_size(string)
    assert tamanho == expected


from colorama import Back

COR_ERRADO = Back.LIGHTRED_EX
COR_CERTO = Back.GREEN
COR_POSICAO = Back.YELLOW
ENDC = Back.RESET


def test_colored_string_iter():
    word = "WoRd"
    colors = [COR_CERTO, COR_ERRADO, COR_POSICAO, ENDC]
    excepted = [
        ("W", COR_CERTO, 0),
        ("o", COR_ERRADO, 1),
        ("R", COR_POSICAO, 2),
        ("d", ENDC, 3),
    ]
    colored_word = ColoredString(word, colors)
    results = list(colored_word)

    assert results == excepted


def test_color_string(presenter):
    word = "W"
    colors = [COR_CERTO]
    excepted = "\033[42mW\033[49m"
    colored_word = ColoredString(word, colors)
    results = presenter.color_string(colored_word)

    assert results == excepted


if __name__ == "__main__":
    pytest.main()
