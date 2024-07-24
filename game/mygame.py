from unidecode import unidecode
import csv
import sys
import random
from colorama import Fore, Back, Style
from game.model.challenge import Challenge
from game.model.hint import *
from game.model.keyboard import Keyboard
from game.viewer.pygame_presenter import PygameCore
from game.viewer.terminal_presenter import TerminalPresenter
from game.viewer.pygame_presenter import pygame_color_dict
from game.viewer.terminal_manipulator import color_dict
from game.solver.word_checker import IWordChecker, WordChecker
from game.model.attempt import Attempt
from game.viewer.terminal_manipulator import IDisplayCore, TerminalCore


###########################################################################
################                                       ####################
################                 JOGO                  ####################
################                                       ####################
###########################################################################


def won_the_game(desafios):
    for desafio in desafios:
        if not desafio.solved:
            return 0
    return 1


def check_valid_word(palavra, palavras):
    return palavra.lower() in palavras.keys()


def sort_words(lista, n):
    palavras_sorteadas = []
    for i in range(n):
        palavra = ""
        while palavra not in palavras_sorteadas:
            random_number = random.randint(1, len(lista) - 1 - 9147)
            palavra = lista[9147 + random_number].upper()
            if palavra not in palavras_sorteadas:
                palavras_sorteadas.append(palavra)

    return palavras_sorteadas


###########################################################################
###########################################################################
################                                       ####################
################                INÍCIO                 ####################
################                                       ####################
###########################################################################
###########################################################################

# ABRE LISTA DE PALAVRAS E REMOVE ACENTUAÇÂO

if __name__ == "__main__":

    # Check if an argument is passed
    if len(sys.argv) > 1:
        try:
            # Convert the argument to an integer and store it in a variable
            n_desafios = int(sys.argv[1])
        except ValueError:
            print("Please pass a valid integer as argument.")
    else:
        n_desafios = 1

    pygame = False
    if len(sys.argv) > 2:
        display_engine = sys.argv[2]
        if display_engine == "pygame":
            pygame = True

    with open("palavras.csv") as csvfile:
        myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        palavras = next(myreader)
    palavras_unidecode = {}
    for palavra in palavras:
        palavras_unidecode[unidecode(palavra)] = palavra
    # n_desafios = 2
    lim_chutes = 5 + n_desafios

    desafios = []
    palavras = sort_words(list(palavras_unidecode.keys()), n_desafios)
    for i in range(n_desafios):
        desafios.append(Challenge(palavras[i]))
    if pygame:
        tmanipulator = PygameCore(pygame_color_dict)
    else:
        tmanipulator = TerminalCore(color_dict)
    grid = [(0, 16 * i) for i in range(n_desafios)]
    presenter = TerminalPresenter(tmanipulator, grid=grid, lim_chutes=lim_chutes)
    presenter.first_print()
    presenter.display_game_screen(desafios)

    ###########################################################################
    ################             MAIN LOOP                 ####################
    ###########################################################################
    padding = 4
    chute_atual = ""
    tentativas = 0
    spacing = 16
    while 1:
        # VISUALIZA
        presenter.display_game_screen(desafios)

        # GANHOU
        if won_the_game(desafios):
            presenter.print_won_the_game(tentativas)  ### mudar a função
            exit(0)

        # PERDEU
        if tentativas == lim_chutes:
            presenter.print_loss_the_game(desafios)  ### mudar a função
            exit(0)

        # INPUT
        chute_atual = presenter.get_input(tentativas, padding)
        if not check_valid_word(chute_atual, palavras_unidecode):
            presenter.print_word_not_accepted(chute_atual)
            continue
        chute_atual = palavras_unidecode[chute_atual.lower()].upper()
        tentativas += 1
        presenter.tmanipulator.clear_line(12)  # Apaga mensagens.

        # CORRIGE
        for i in range(len(desafios)):
            if not desafios[i].solved:
                desafios[i].update(unidecode(chute_atual))
