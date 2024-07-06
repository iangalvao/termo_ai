import pytest
from game.word_checker import WordChecker, Hint

# test_my_module.py


def test_get_feedback_from_guess_recebe_chute_sem_letras_certa_e_devolve_correcao_sem_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "FGHIJ"
    esperado = [
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_todas_letras_na_pos_certa_e_devolve_correcao_com_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "ABCDE"
    esperado = [
        RIGHT_POS,
        RIGHT_POS,
        RIGHT_POS,
        RIGHT_POS,
        RIGHT_POS,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_todas_letras_na_pos_errada_e_devolve_correcao_com_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "BCDEA"
    esperado = [
        WRONG_POS,
        WRONG_POS,
        WRONG_POS,
        WRONG_POS,
        WRONG_POS,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_uma_letras_na_pos_certa_e_devolve_correcao_com_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "AGHIJ"
    esperado = [
        RIGHT_POS,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_uma_letras_na_pos_errada_e_devolve_correcao_com_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "GAHIJ"
    esperado = [
        WRONG_LETTER,
        WRONG_POS,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_duas_letras_na_pos_certa_e_devolve_correcao_com_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "ABHIJ"
    esperado = [
        RIGHT_POS,
        RIGHT_POS,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_duas_letras_na_pos_errada_e_devolve_correcao_com_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "GABIJ"
    esperado = [
        WRONG_LETTER,
        WRONG_POS,
        WRONG_POS,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_duas_letras_iguais_na_pos_errada_de_uma_palavra_com_uma_unica_dessa_letra_devolve_correcao_com_uma_dica_de_posicao():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "GAAHI"
    esperado = [
        WRONG_LETTER,
        WRONG_POS,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_duas_letras_iguais_na_pos_errada_de_uma_palavra_com_uma_unica_dessa_letra__depois_da_pos_chutada_devolve_correcao_com_uma_dica_de_posicao():
    word_checker = WordChecker()
    palavra = "BCDEA"
    chute = "GAAHI"
    esperado = [
        WRONG_LETTER,
        WRONG_POS,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_uma_letra_na_posicao_certa_e_uma_na_pos_errada_de_uma_palavra_com_duas_dessa_letra_devolve_correcao_com_uma_dica_de_posicao():
    word_checker = WordChecker()
    palavra = "AACDE"
    chute = "GAAHI"
    esperado = [
        WRONG_LETTER,
        RIGHT_POS,
        WRONG_POS,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_uma_letra_na_posicao_certa_e_uma_na_pos_errada_de_uma_palavra_com_duas_dessa_letra_com_ocorrencia_depois_da_pos_errada_e_devolve_correcao_com_uma_dicas():
    word_checker = WordChecker()
    palavra = "BCAAD"
    chute = "GAAHI"
    esperado = [
        WRONG_LETTER,
        WRONG_POS,
        RIGHT_POS,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_uma_letra_na_posicao_certa_e_uma_na_pos_errada_de_uma_palavra_com_duas_dessa_letra_com_ocorrencia_entre_a_pos_errada_e__a_certa_e_devolve_correcao_com_uma_dicas():
    word_checker = WordChecker()
    palavra = "BAFAD"
    chute = "GAAHI"
    esperado = [
        WRONG_LETTER,
        RIGHT_POS,
        WRONG_POS,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]
