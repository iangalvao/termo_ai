import pytest

from game.model.attempt import Attempt
from game.model.hint import RIGHT_POS, WRONG_LETTER, WRONG_POS, UNKNOWN_LETTER
from game.model.keyboard import Keyboard
from game.model.challenge import Challenge
from game.viewer.terminal_manipulator import (
    COR_CERTO,
    ENDC,
    COR_POSICAO,
    COR_ERRADO,
    ColoredString,
)
from game.viewer.game_display import UNDERLINE, Screen, TerminalPresenter


@pytest.fixture
def words():
    return ["abada", "arara", "abade", "qwert", "yuiop", "ghjkl", "arame"]


@pytest.fixture
def attempts(words):
    return [Attempt(w, "arame") for w in words]


@pytest.fixture
def challenge_full(attempts):
    d = Challenge("arame", None)
    d.attempts = attempts
    return [d]


@pytest.fixture
def challenge_half(attempts):
    d = Challenge("arame", None)
    d.attempts = attempts[:3]
    return [d]


@pytest.fixture
def challenge_empty():
    d = Challenge("arame", None)
    return [d]


@pytest.fixture
def colors():
    return [
        [COR_CERTO, COR_ERRADO, COR_CERTO, COR_ERRADO, COR_ERRADO],
        [COR_CERTO, COR_CERTO, COR_CERTO, COR_ERRADO, COR_ERRADO],
        [COR_CERTO, COR_ERRADO, COR_CERTO, COR_ERRADO, COR_CERTO],
        [COR_ERRADO, COR_ERRADO, COR_POSICAO, COR_POSICAO, COR_ERRADO],
        [
            COR_ERRADO,
            COR_ERRADO,
            COR_ERRADO,
            COR_ERRADO,
            COR_ERRADO,
        ],
        [
            COR_ERRADO,
            COR_ERRADO,
            COR_ERRADO,
            COR_ERRADO,
            COR_ERRADO,
        ],
        [COR_CERTO, COR_CERTO, COR_CERTO, COR_CERTO, COR_CERTO],
    ]


@pytest.fixture
def expected_screen_full(words, colors):
    s = Screen()
    for n, (word, color) in enumerate(zip(words, colors)):
        s.add(ColoredString(word, color), (n + 1, 6))
    return s


@pytest.fixture
def expected_screen_half(words, colors):
    s = Screen()
    for n, (word, color) in enumerate(zip(words[:3], colors[:3])):
        s.add(ColoredString(word, color), (n + 1, 6))
    for i in range(3, 6):
        s.add(ColoredString("_____", [ENDC for i in range(6)]), (i + 1, 6))
    return s


@pytest.fixture
def expected_screen_empty(words, colors):
    s = Screen()
    for i in range(6):
        s.add(ColoredString("_____", [ENDC for i in range(6)]), (i + 1, 6))
    return s


@pytest.fixture
def keyboard():
    return Keyboard()


@pytest.fixture
def qwerty_only_keyboard(keyboard: Keyboard):
    for keyline, pos in keyboard:
        for char, hint in keyline:
            if char not in "QWERTY":
                keyboard.set_letter_hint(char, WRONG_LETTER)
            else:
                keyboard.set_letter_hint(char, RIGHT_POS)
    return keyboard


@pytest.fixture
def expected_qwerty_keyboard_screen():
    screen = Screen()
    first_line = ColoredString(
        "QWERTY    ", [COR_CERTO for c in "QWERTY"] + [COR_ERRADO for c in "UIOP"]
    )
    second_line_chars = "ASDFGHJKL"
    second_line = ColoredString("         ", [COR_ERRADO for c in second_line_chars])
    third_line_chards = "ZXCVBNM"
    third_line = ColoredString("       ", [COR_ERRADO for c in third_line_chards])
    screen.add(first_line, (0, 0))
    screen.add(second_line, (1, 0))
    screen.add(third_line, (2, 0))
    return screen


@pytest.fixture
def expected_empty_keyboard_screen():
    screen = Screen()
    first_line_chars = "QWERTYUIOP"
    first_line = ColoredString(first_line_chars, [ENDC for c in first_line_chars])
    second_line_chars = "ASDFGHJKL"
    second_line = ColoredString(second_line_chars, [ENDC for c in second_line_chars])
    third_line_chards = "ZXCVBNM"
    third_line = ColoredString(third_line_chards, [ENDC for c in third_line_chards])
    screen.add(first_line, (0, 0))
    screen.add(second_line, (1, 0))
    screen.add(third_line, (2, 0))
    return screen


def test_keyboard_screen_empty(keyboard, expected_empty_keyboard_screen):
    tPresenter = TerminalPresenter(None)
    screen = tPresenter.keyboard(keyboard, (0, 0))
    assert (
        screen == expected_empty_keyboard_screen
    ), f"\nEXPECTED SCREEN:\n{expected_empty_keyboard_screen}\nGOT:\n{screen}"


def test_keyboard_screen_qwerty(qwerty_only_keyboard, expected_qwerty_keyboard_screen):
    tPresenter = TerminalPresenter(None)
    screen = tPresenter.keyboard(qwerty_only_keyboard, (0, 0))
    assert (
        screen == expected_qwerty_keyboard_screen
    ), f"\nEXPECTED SCREEN:\n{expected_qwerty_keyboard_screen}\nGOT:\n{screen}"


def test_game_screen_full(challenge_full, expected_screen_full):
    tPresenter = TerminalPresenter(None)
    challenge_number = 0
    lim_guesses = 6
    screen = tPresenter.table_screen(challenge_full[0], challenge_number, lim_guesses)

    assert screen == expected_screen_full


def test_game_screen_half(challenge_half, expected_screen_half):
    tPresenter = TerminalPresenter(None)
    challenge_number = 0
    lim_guesses = 6
    screen = tPresenter.table_screen(challenge_half[0], challenge_number, lim_guesses)

    assert len(list(screen)) == len(list((expected_screen_half)))
    for (stringA, posA), (stringB, posB) in zip(screen, expected_screen_half):
        assert stringA.str == stringB.str
        assert stringA.colors == stringB.colors
        assert posA == posB
