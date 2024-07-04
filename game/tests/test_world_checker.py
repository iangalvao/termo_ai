import pytest
from game.word_checker import WordChecker, Hint

# test_my_module.py


def test_get_feedback_from_guess_recebe_chute_sem_letras_certa_e_devolve_correcao_sem_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "FGHIJ"
    esperado = [
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_todas_letras_na_pos_certa_e_devolve_correcao_com_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "ABCDE"
    esperado = [
        Hint.RIGHT_POS,
        Hint.RIGHT_POS,
        Hint.RIGHT_POS,
        Hint.RIGHT_POS,
        Hint.RIGHT_POS,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_todas_letras_na_pos_errada_e_devolve_correcao_com_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "BCDEA"
    esperado = [
        Hint.WRONG_POS,
        Hint.WRONG_POS,
        Hint.WRONG_POS,
        Hint.WRONG_POS,
        Hint.WRONG_POS,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_uma_letras_na_pos_certa_e_devolve_correcao_com_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "AGHIJ"
    esperado = [
        Hint.RIGHT_POS,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_uma_letras_na_pos_errada_e_devolve_correcao_com_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "GAHIJ"
    esperado = [
        Hint.WRONG_LETTER,
        Hint.WRONG_POS,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_duas_letras_na_pos_certa_e_devolve_correcao_com_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "ABHIJ"
    esperado = [
        Hint.RIGHT_POS,
        Hint.RIGHT_POS,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_duas_letras_na_pos_errada_e_devolve_correcao_com_dicas():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "GABIJ"
    esperado = [
        Hint.WRONG_LETTER,
        Hint.WRONG_POS,
        Hint.WRONG_POS,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_duas_letras_iguais_na_pos_errada_de_uma_palavra_com_uma_unica_dessa_letra_devolve_correcao_com_uma_dica_de_posicao():
    word_checker = WordChecker()
    palavra = "ABCDE"
    chute = "GAAHI"
    esperado = [
        Hint.WRONG_LETTER,
        Hint.WRONG_POS,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_duas_letras_iguais_na_pos_errada_de_uma_palavra_com_uma_unica_dessa_letra__depois_da_pos_chutada_devolve_correcao_com_uma_dica_de_posicao():
    word_checker = WordChecker()
    palavra = "BCDEA"
    chute = "GAAHI"
    esperado = [
        Hint.WRONG_LETTER,
        Hint.WRONG_POS,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_uma_letra_na_posicao_certa_e_uma_na_pos_errada_de_uma_palavra_com_duas_dessa_letra_devolve_correcao_com_uma_dica_de_posicao():
    word_checker = WordChecker()
    palavra = "AACDE"
    chute = "GAAHI"
    esperado = [
        Hint.WRONG_LETTER,
        Hint.RIGHT_POS,
        Hint.WRONG_POS,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_uma_letra_na_posicao_certa_e_uma_na_pos_errada_de_uma_palavra_com_duas_dessa_letra_com_ocorrencia_depois_da_pos_errada_e_devolve_correcao_com_uma_dicas():
    word_checker = WordChecker()
    palavra = "BCAAD"
    chute = "GAAHI"
    esperado = [
        Hint.WRONG_LETTER,
        Hint.WRONG_POS,
        Hint.RIGHT_POS,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]


def test_get_feedback_from_guess_recebe_chute_com_uma_letra_na_posicao_certa_e_uma_na_pos_errada_de_uma_palavra_com_duas_dessa_letra_com_ocorrencia_entre_a_pos_errada_e__a_certa_e_devolve_correcao_com_uma_dicas():
    word_checker = WordChecker()
    palavra = "BAFAD"
    chute = "GAAHI"
    esperado = [
        Hint.WRONG_LETTER,
        Hint.RIGHT_POS,
        Hint.WRONG_POS,
        Hint.WRONG_LETTER,
        Hint.WRONG_LETTER,
    ]

    check_word = word_checker.get_feedback_from_guess(chute, palavra)
    for i in range(len(esperado)):
        assert check_word[i] == esperado[i]
