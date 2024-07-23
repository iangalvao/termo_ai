import pytest
from game.model.attempt import Attempt
from game.solver.word_checker import WordChecker
from game.model.hint import *

# test_my_module.py


def test_get_feedback_from_guess_recebe_chute_sem_letras_certa_e_devolve_correcao_sem_dicas():
    palavra = "ABCDE"
    chute = "FGHIJ"
    attempt = Attempt(chute, palavra)
    esperado = [
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = attempt.feedbacks
    assert check_word == esperado, f"Failed. Expected {esperado} got {check_word}"


def test_get_feedback_from_guess_recebe_chute_com_todas_letras_na_pos_certa_e_devolve_correcao_com_dicas():
    palavra = "ABCDE"
    chute = "ABCDE"
    attempt = Attempt(chute, palavra)
    esperado = [
        RIGHT_POS,
        RIGHT_POS,
        RIGHT_POS,
        RIGHT_POS,
        RIGHT_POS,
    ]

    check_word = attempt.feedbacks
    assert check_word == esperado, f"Failed. Expected {esperado} got {check_word}"


def test_get_feedback_from_guess_recebe_chute_com_todas_letras_na_pos_errada_e_devolve_correcao_com_dicas():
    palavra = "ABCDE"
    chute = "BCDEA"
    attempt = Attempt(chute, palavra)
    esperado = [
        WRONG_POS,
        WRONG_POS,
        WRONG_POS,
        WRONG_POS,
        WRONG_POS,
    ]

    check_word = attempt.feedbacks
    assert check_word == esperado, f"Failed. Expected {esperado} got {check_word}"


def test_get_feedback_from_guess_recebe_chute_com_uma_letras_na_pos_certa_e_devolve_correcao_com_dicas():
    palavra = "ABCDE"
    chute = "AGHIJ"
    attempt = Attempt(chute, palavra)
    esperado = [
        RIGHT_POS,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = attempt.feedbacks
    assert check_word == esperado, f"Failed. Expected {esperado} got {check_word}"


def test_get_feedback_from_guess_recebe_chute_com_uma_letras_na_pos_errada_e_devolve_correcao_com_dicas():
    palavra = "ABCDE"
    chute = "GAHIJ"
    attempt = Attempt(chute, palavra)
    esperado = [
        WRONG_LETTER,
        WRONG_POS,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = attempt.feedbacks
    assert check_word == esperado, f"Failed. Expected {esperado} got {check_word}"


def test_get_feedback_from_guess_recebe_chute_com_duas_letras_na_pos_certa_e_devolve_correcao_com_dicas():
    palavra = "ABCDE"
    chute = "ABHIJ"
    attempt = Attempt(chute, palavra)
    esperado = [
        RIGHT_POS,
        RIGHT_POS,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = attempt.feedbacks
    assert check_word == esperado, f"Failed. Expected {esperado} got {check_word}"


def test_get_feedback_from_guess_recebe_chute_com_duas_letras_na_pos_errada_e_devolve_correcao_com_dicas():
    palavra = "ABCDE"
    chute = "GABIJ"
    attempt = Attempt(chute, palavra)
    esperado = [
        WRONG_LETTER,
        WRONG_POS,
        WRONG_POS,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = attempt.feedbacks
    assert check_word == esperado, f"Failed. Expected {esperado} got {check_word}"


def test_get_feedback_from_guess_recebe_chute_com_duas_letras_iguais_na_pos_errada_de_uma_palavra_com_uma_unica_dessa_letra_devolve_correcao_com_uma_dica_de_posicao():
    palavra = "ABCDE"
    chute = "GAAHI"
    attempt = Attempt(chute, palavra)
    esperado = [
        WRONG_LETTER,
        WRONG_POS,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = attempt.feedbacks
    assert check_word == esperado, f"Failed. Expected {esperado} got {check_word}"


def test_get_feedback_from_guess_recebe_chute_com_duas_letras_iguais_na_pos_errada_de_uma_palavra_com_uma_unica_dessa_letra_depois_da_pos_chutada_devolve_correcao_com_uma_dica_de_posicao():
    palavra = "BCDEA"
    chute = "GAAHI"
    attempt = Attempt(chute, palavra)
    esperado = [
        WRONG_LETTER,
        WRONG_POS,
        WRONG_LETTER,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = attempt.feedbacks
    assert check_word == esperado, f"Failed. Expected {esperado} got {check_word}"


def test_get_feedback_from_guess_recebe_chute_com_uma_letra_na_posicao_certa_e_uma_na_pos_errada_de_uma_palavra_com_duas_dessa_letra_devolve_correcao_com_uma_dica_de_posicao():
    palavra = "AACDE"
    chute = "GAAHI"
    attempt = Attempt(chute, palavra)
    esperado = [
        WRONG_LETTER,
        RIGHT_POS,
        WRONG_POS,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = attempt.feedbacks
    assert check_word == esperado, f"Failed. Expected {esperado} got {check_word}"


def test_get_feedback_from_guess_recebe_chute_com_uma_letra_na_posicao_certa_e_uma_na_pos_errada_de_uma_palavra_com_duas_dessa_letra_com_ocorrencia_depois_da_pos_errada_e_devolve_correcao_com_uma_dicas():
    palavra = "BCAAD"
    chute = "GAAHI"
    attempt = Attempt(chute, palavra)
    esperado = [
        WRONG_LETTER,
        WRONG_POS,
        RIGHT_POS,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = attempt.feedbacks
    assert check_word == esperado, f"Failed. Expected {esperado} got {check_word}"


def test_get_feedback_from_guess_recebe_chute_com_uma_letra_na_posicao_certa_e_uma_na_pos_errada_de_uma_palavra_com_duas_dessa_letra_com_ocorrencia_entre_a_pos_errada_e__a_certa_e_devolve_correcao_com_uma_dicas():
    palavra = "BAFAD"
    chute = "GAAHI"
    attempt = Attempt(chute, palavra)
    esperado = [
        WRONG_LETTER,
        RIGHT_POS,
        WRONG_POS,
        WRONG_LETTER,
        WRONG_LETTER,
    ]

    check_word = attempt.feedbacks
    assert check_word == esperado, f"Failed. Expected {esperado} got {check_word}"
