import pytest
from game.solver.solver_tools import WordFilter
from game.common import Hint

# test_my_module.py


@pytest.mark.parametrize(
    "string, expected",
    [("s", 1), ("á", 1), ("sapos", 5), ("     ", 5)],
)
def test_fil(string, expected):
    t = TerminalPresenter()
    string = "\033[1C" + string
    tamanho = t.tamanho_string(string)
    assert tamanho == expected


@pytest.mark.parametrize(
    "string, expected",
    [("s", 1), ("á", 1), ("sapos", 5), ("     ", 5)],
)
def test_tamanho_string_recebe_sem_formatacao(string, expected):
    t = TerminalPresenter()
    tamanho = t.tamanho_string(string)
    assert tamanho == expected


def filter_from_hint(
    self, hint: Hint, letter: str, val: int, original_words: list[str]
):
    pass
