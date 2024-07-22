import pytest

from game.attempt import Attempt
from game.hint import RIGHT_POS, WRONG_LETTER, WRONG_POS, UNKNOWN_LETTER
from game.mygame import Desafio
from game.terminal_manipulator import ColoredString
from game.terminal_presenter import Screen, TerminalPresenter


@pytest.fixture
def words():
    return ["abada", "arara", "abade", "qwert", "yuiop", "ghjkl", "arame"]


@pytest.fixture
def attempts(words):
    return [Attempt(w, "arame") for w in words]


@pytest.fixture
def full_challenge(attempts):
    d = Desafio("arame", None)
    d.attempts = attempts
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
    return s


def test_game_screen(full_challenge, expected_screen_full):
    tPresenter = TerminalPresenter(None)
    screen = tPresenter.game_screen(full_challenge)

    assert screen == expected_screen_full
