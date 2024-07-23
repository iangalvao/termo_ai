from unidecode import unidecode
import csv
import sys
import random
from colorama import Fore, Back, Style
from game.hint import *
from game.keyboard import Keyboard
from game.terminal_presenter import TerminalPresenter
from game.terminal_manipulator import color_dict
from game.word_checker import IWordChecker, WordChecker
from game.attempt import Attempt
from game.terminal_manipulator import ITerminalManipulator, TerminalManipulator


###########################################################################
################                  DESAFIO              ####################
###########################################################################


class Desafio:
    def __init__(self, palavra, word_checker: IWordChecker, lim_guesses=6) -> None:
        self.chutes = []
        self.feedbacks = []
        self.attempts: list[Attempt] = []
        self.teclado = Keyboard()
        self.palavra = palavra
        self.solved = 0
        self.word_checker: IWordChecker = word_checker
        self.lim_guesses = 6

    def get_lim_guesses(self):
        return self.lim_guesses

    def get_keyboard(self):
        return self.teclado

    def get_attempts(self):
        return self.attempts

    def update(self, chute):
        if chute == self.palavra:
            self.solved = 1
        attempt = Attempt(chute, self.palavra)
        self.attempts.append(attempt)

        chute_corrigido = self.word_checker.get_feedback_from_guess(
            unidecode(chute.lower()), unidecode(self.palavra.lower())
        )
        self.chutes.append(chute)
        self.feedbacks.append(chute_corrigido)

        self.teclado.process_hints(attempt)
        # self.teclado.process_hints(chute, chute_corrigido)
        return chute_corrigido


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

    with open("palavras.csv") as csvfile:
        myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        palavras = next(myreader)
    palavras_unidecode = {}
    for palavra in palavras:
        palavras_unidecode[unidecode(palavra)] = palavra
    # n_desafios = 2
    lim_chutes = 5 + n_desafios

    word_checker = WordChecker()
    desafios = []
    palavras = sort_words(list(palavras_unidecode.keys()), n_desafios)
    for i in range(n_desafios):
        desafios.append(Desafio(palavras[i], word_checker))
    tmanipulator = TerminalManipulator(color_dict)
    presenter = TerminalPresenter(tmanipulator)
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
        # for i in range(len(desafios)):
        #     teclado_linhas = desafios[i].teclado.get_keyboard_lines_with_hints()
        #     presenter.print_game_at_pos(
        #         desafios[i].chutes,
        #         teclado_linhas,
        #         (0, padding + i * spacing),
        #         desafios[i].feedbacks,
        #     )

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
