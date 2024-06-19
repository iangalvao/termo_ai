import pytest
from game import TerminalPresenter, Desafio

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


def test_check_word_recebe_chute_sem_letras_certa_e_devolve_correcao_sem_dicas():
    desafio = Desafio("ABCDE")
    chute = "FGHIJ"
    esperado = [("F", 0), ("G", 0), ("H", 0), ("I", 0), ("J", 0)]

    check_word = desafio.check_word(chute)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_check_word_recebe_chute_com_todas_letras_na_pos_certa_e_devolve_correcao_com_dicas():
    desafio = Desafio("ABCDE")
    chute = "ABCDE"
    esperado = [("A", 2), ("B", 2), ("C", 2), ("D", 2), ("E", 2)]

    check_word = desafio.check_word(chute)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_check_word_recebe_chute_com_todas_letras_na_pos_errada_e_devolve_correcao_com_dicas():
    desafio = Desafio("ABCDE")
    chute = "BCDEA"
    esperado = [("B", 1), ("C", 1), ("D", 1), ("E", 1), ("A", 1)]

    check_word = desafio.check_word(chute)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_check_word_recebe_chute_com_uma_letras_na_pos_certa_e_devolve_correcao_com_dicas():
    desafio = Desafio("ABCDE")
    chute = "AGHIJ"
    esperado = [("A", 2), ("G", 0), ("H", 0), ("I", 0), ("J", 0)]

    check_word = desafio.check_word(chute)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_check_word_recebe_chute_com_uma_letras_na_pos_errada_e_devolve_correcao_com_dicas():
    desafio = Desafio("ABCDE")
    chute = "GAHIJ"
    esperado = [("G", 0), ("A", 1), ("H", 0), ("I", 0), ("J", 0)]

    check_word = desafio.check_word(chute)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_check_word_recebe_chute_com_duas_letras_na_pos_certa_e_devolve_correcao_com_dicas():
    desafio = Desafio("ABCDE")
    chute = "ABHIJ"
    esperado = [("A", 2), ("B", 2), ("H", 0), ("I", 0), ("J", 0)]

    check_word = desafio.check_word(chute)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_check_word_recebe_chute_com_duas_letras_na_pos_errada_e_devolve_correcao_com_dicas():
    desafio = Desafio("ABCDE")
    chute = "GABIJ"
    esperado = [("G", 0), ("A", 1), ("B", 1), ("I", 0), ("J", 0)]

    check_word = desafio.check_word(chute)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_check_word_recebe_chute_com_duas_letras_iguais_na_pos_errada_de_uma_palavra_com_uma_unica_dessa_letra_devolve_correcao_com_uma_dica_de_posicao():
    desafio = Desafio("ABCDE")
    chute = "GAAHI"
    esperado = [("G", 0), ("A", 1), ("A", 0), ("H", 0), ("I", 0)]

    check_word = desafio.check_word(chute)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_check_word_recebe_chute_com_duas_letras_iguais_na_pos_errada_de_uma_palavra_com_uma_unica_dessa_letra__depois_da_pos_chutada_devolve_correcao_com_uma_dica_de_posicao():
    desafio = Desafio("BCDEA")
    chute = "GAAHI"
    esperado = [("G", 0), ("A", 1), ("A", 0), ("H", 0), ("I", 0)]

    check_word = desafio.check_word(chute)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_check_word_recebe_chute_com_uma_letra_na_posicao_certa_e_uma_na_pos_errada_de_uma_palavra_com_duas_dessa_letra_devolve_correcao_com_uma_dica_de_posicao():
    desafio = Desafio("AACDE")
    chute = "GAAHI"
    esperado = [("G", 0), ("A", 2), ("A", 1), ("H", 0), ("I", 0)]

    check_word = desafio.check_word(chute)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_check_word_recebe_chute_com_uma_letra_na_posicao_certa_e_uma_na_pos_errada_de_uma_palavra_com_duas_dessa_letra_com_ocorrencia_depois_da_pos_errada_e_devolve_correcao_com_uma_dicas():
    desafio = Desafio("BCAAD")
    chute = "GAAHI"
    esperado = [("G", 0), ("A", 1), ("A", 2), ("H", 0), ("I", 0)]

    check_word = desafio.check_word(chute)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_check_word_recebe_chute_com_uma_letra_na_posicao_certa_e_uma_na_pos_errada_de_uma_palavra_com_duas_dessa_letra_com_ocorrencia_entre_a_pos_errada_e__a_certa_e_devolve_correcao_com_uma_dicas():
    desafio = Desafio("BAFAD")
    chute = "GAAHI"
    esperado = [("G", 0), ("A", 2), ("A", 1), ("H", 0), ("I", 0)]

    check_word = desafio.check_word(chute)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]
