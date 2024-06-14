import pytest
from game import TerminalPresenter

# test_my_module.py


@pytest.mark.parametrize(
    "string, expected",
    [("s", 1), ("á", 1), ("sapos", 5), ("     ", 5)],
)
def test_tamanho_string_recebe_formatacao_de_posicionamento(string, expected):
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


@pytest.mark.parametrize(
    "cor, string, expected",
    [
        ("\033[93m", "s", 1),
        ("\033[93m", "á", 1),
        ("\033[93m", "sapos", 5),
        ("\033[93m", "     ", 5),
    ],
)
def test_tamanho_string_recebe_formatacao_de_cor_com_duas_casas_numericas_apos_colchete(
    cor, string, expected
):
    t = TerminalPresenter()
    string = cor + string
    tamanho = t.tamanho_string(string)
    assert tamanho == expected


def test_tamanho_string_recebe_linha_de_taclas_coloridas():
    s = "\033[94mQ\033[0m\033[94mW\033[0m"
    t = TerminalPresenter()
    tamanho = t.tamanho_string(s)
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
def test_tamanho_string_recebe_formatacao_de_cor_com_tres_casas_numericas_apos_colchete(
    cor, string, expected
):
    t = TerminalPresenter()
    string = cor + string
    tamanho = t.tamanho_string(string)
    assert tamanho == expected
