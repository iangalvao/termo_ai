import pytest

from game.attempt import Attempt
from game.hint import RIGHT_POS, WRONG_LETTER, WRONG_POS, UNKNOWN_LETTER
from game.keyboard import Keyboard
from game.mygame import Desafio
from game.terminal_manipulator import ColoredString
from game.terminal_presenter import UNDERLINE, Screen, TerminalPresenter


@pytest.fixture
def words():
    return ["abada", "arara", "abade", "qwert", "yuiop", "ghjkl", "arame"]


@pytest.fixture
def attempts(words):
    return [Attempt(w, "arame") for w in words]


@pytest.fixture
def challenge_full(attempts):
    d = Desafio("arame", None)
    d.attempts = attempts
    return [d]


@pytest.fixture
def challenge_half(attempts):
    d = Desafio("arame", None)
    d.attempts = attempts[:3]
    return [d]


@pytest.fixture
def challenge_empty():
    d = Desafio("arame", None)
    return [d]


@pytest.fixture
def colors():
    return [
        [RIGHT_POS, UNKNOWN_LETTER, RIGHT_POS, UNKNOWN_LETTER, UNKNOWN_LETTER],
        [RIGHT_POS, RIGHT_POS, RIGHT_POS, UNKNOWN_LETTER, UNKNOWN_LETTER],
        [RIGHT_POS, UNKNOWN_LETTER, RIGHT_POS, UNKNOWN_LETTER, RIGHT_POS],
        [UNKNOWN_LETTER, UNKNOWN_LETTER, WRONG_POS, WRONG_POS, UNKNOWN_LETTER],
        [
            UNKNOWN_LETTER,
            UNKNOWN_LETTER,
            UNKNOWN_LETTER,
            UNKNOWN_LETTER,
            UNKNOWN_LETTER,
        ],
        [
            UNKNOWN_LETTER,
            UNKNOWN_LETTER,
            UNKNOWN_LETTER,
            UNKNOWN_LETTER,
            UNKNOWN_LETTER,
        ],
        [RIGHT_POS, RIGHT_POS, RIGHT_POS, RIGHT_POS, RIGHT_POS],
    ]


@pytest.fixture
def expected_screen_full(words, colors):
    s = Screen()
    for n, (word, color) in enumerate(zip(words, colors)):
        s.add(ColoredString(word, color), (n, 0))
    return s


@pytest.fixture
def expected_screen_half(words, colors):
    s = Screen()
    for n, (word, color) in enumerate(zip(words[:3], colors[:3])):
        s.add(ColoredString(word, color), (n, 0))
    for i in range(3, 6):
        s.add(ColoredString("     ", [UNDERLINE for i in range(6)]), (i, 0))
    return s


@pytest.fixture
def expected_screen_empty(words, colors):
    s = Screen()
    for i in range(6):
        s.add(ColoredString("     ", [UNDERLINE for i in range(6)]), (i, 0))
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
        "QWERTYUIOP", [RIGHT_POS for c in "QWERTY"] + [UNKNOWN_LETTER for c in "UIOP"]
    )
    second_line_chars = "ASDFGHJKL"
    second_line = ColoredString(
        second_line_chars, [UNKNOWN_LETTER for c in second_line_chars]
    )
    third_line_chards = "ZXCVBNM"
    third_line = ColoredString(
        third_line_chards, [UNKNOWN_LETTER for c in third_line_chards]
    )
    screen.add(first_line, (10, 0))
    screen.add(second_line, (11, 0))
    screen.add(third_line, (12, 0))
    return screen


@pytest.fixture
def expected_empty_keyboard_screen():
    screen = Screen()
    first_line_chars = "QWERTYUIOP"
    first_line = ColoredString(
        first_line_chars, [UNKNOWN_LETTER for c in first_line_chars]
    )
    second_line_chars = "ASDFGHJKL"
    second_line = ColoredString(
        second_line_chars, [UNKNOWN_LETTER for c in second_line_chars]
    )
    third_line_chards = "ZXCVBNM"
    third_line = ColoredString(
        third_line_chards, [UNKNOWN_LETTER for c in third_line_chards]
    )
    screen.add(first_line, (10, 0))
    screen.add(second_line, (11, 0))
    screen.add(third_line, (12, 0))
    return screen


def test_keyboard_screen_empty(keyboard, expected_empty_keyboard_screen):
    tPresenter = TerminalPresenter(None)
    screen = tPresenter.keyboard(keyboard, (0, 0))
    assert (
        screen == expected_empty_keyboard_screen
    ), f"\nEXPECTED SCREEN: {expected_empty_keyboard_screen}\nGOT: {screen}"


def test_keyboard_screen_qwerty(qwerty_only_keyboard, expected_qwerty_keyboard_screen):
    tPresenter = TerminalPresenter(None)
    screen = tPresenter.keyboard(qwerty_only_keyboard, (0, 0))
    assert (
        screen == expected_qwerty_keyboard_screen
    ), f"\nEXPECTED SCREEN: {expected_qwerty_keyboard_screen}\nGOT: {screen}"


def test_game_screen_full(challenge_full, expected_screen_full):
    tPresenter = TerminalPresenter(None)
    screen = tPresenter.game_screen(challenge_full)

    assert screen == expected_screen_full


def test_game_screen_half(challenge_half, expected_screen_half):
    tPresenter = TerminalPresenter(None)
    screen = tPresenter.game_screen(challenge_half)

    assert len(list(screen)) == len(list((expected_screen_half)))
    for (stringA, posA), (stringB, posB) in zip(screen, expected_screen_half):
        assert stringA.str == stringB.str
        assert stringA.colors == stringB.colors
        assert posA == posB
