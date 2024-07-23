import pytest

from game.attempt import Attempt
from game.hint import RIGHT_POS, WRONG_LETTER, WRONG_POS, UNKNOWN_LETTER
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
