from unidecode import unidecode
import csv
import sys
import random
from colorama import Fore, Back, Style
from game.hint import *
from game.keyboard import Keyboard
from game.word_checker import IWordChecker, WordChecker
from game.attempt import Attempt
from game.terminal_manipulator import ITerminalManipulator, TerminalManipulator

###########################################################################
################           ESTILO DO TERMINAL          ####################
###########################################################################


# CORES PARA VISUALIZAÇÂO NO TERMINAL
bcolors = {
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKCYAN": "\033[96m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
}

UNDERLINE = "\033[4m"
END_UNDERLINE = "\033[0m"
COR_ERRADO = Back.LIGHTRED_EX
COR_CERTO = Back.GREEN
COR_POSICAO = Back.YELLOW
ENDC = Back.RESET

# CÒDIGOS PARA CORREÇÂO DE CADA LETRA
LETRA_DESCONHECIDA = -1
LETRA_INCORRETA = 0
POS_INCORRETA = 1
CERTO = 2

cores_das_dicas = {
    UNKNOWN_LETTER: ENDC,
    WRONG_LETTER: COR_ERRADO,
    WRONG_POS: COR_POSICAO,
    RIGHT_POS: COR_CERTO,
}


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


###########################################################################
################                                       ####################
################                LÓGICA                 ####################
################                                       ####################
###########################################################################


###########################################################################
################            CHECAGEM DE LETRAS         ####################
###########################################################################


class Desafio:
    def __init__(self, palavra, word_checker: IWordChecker) -> None:
        self.chutes = []
        self.feedbacks = []
        self.attempts: list[Attempt] = []
        self.teclado = Keyboard()
        self.palavra = palavra
        self.solved = 0
        self.word_checker: IWordChecker = word_checker

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
###########################################################################
################                                       ####################
################             VISUALIZAÇÂO              ####################
################                                       ####################
###########################################################################
###########################################################################


###########################################################################
################          MANIPULAÇÂO DO CURSOR        ####################
###########################################################################


class TerminalPresenter:
    def __init__(self, tmanipulator: ITerminalManipulator) -> None:
        self.tmanipulator = tmanipulator

    ###########################################################################
    ################           TELA PRINCIPAL              ####################
    ###########################################################################

    ################               CHUTES                  ####################

    def print_tabela(self, n):
        for i in range(lim_chutes - n):
            self.tmanipulator.print_at_pos(
                UNDERLINE + "     " + END_UNDERLINE, (i + n + 1, 2)
            )

    def print_chutes(self, chutes, feedbacks):
        chutes_coloridos = self.colore_lista_chutes(chutes, feedbacks)
        for i in range(len(chutes_coloridos)):
            self.tmanipulator.print_at_pos(chutes_coloridos[i], (i + 1, 2))

    def colore_lista_chutes(self, chutes, feedbacks):
        chutes_coloridos = []
        for i, chute in enumerate(chutes):
            chutes_colorido = ""
            feedback = feedbacks[i]
            for pos, letra in enumerate(chute):
                dica = feedback[pos]
                if dica == WRONG_LETTER:
                    dica = UNKNOWN_LETTER
                cor = cores_das_dicas[dica]
                letra_colorida = f"{cor}{letra}{ENDC}"
                chutes_colorido += letra_colorida
            chutes_coloridos.append(chutes_colorido)
        return chutes_coloridos

    #################                TECLADO                  ####################
    def print_keyboard(self, linhas_teclado_dicas):
        linhas_teclas_coloridas = self.color_keyboard_lines(linhas_teclado_dicas)
        for i in range(3):
            linha_colorida = linhas_teclas_coloridas[i]
            if i == 2:
                # A última linha começa uma casa depois por escolha de diagramação.
                linha_colorida = " " + linha_colorida
            self.tmanipulator.print_at_pos(
                linhas_teclas_coloridas[i], (lim_chutes + 2 + i, 0)
            )

    def color_keyboard_lines(self, linhas_de_teclas_com_dicas):
        linhas_de_teclas_coloridas = []
        for linha in linhas_de_teclas_com_dicas:
            linha_colorida = ""
            for letra, dica in linha:
                cor = cores_das_dicas[dica]
                if cor == cores_das_dicas[WRONG_LETTER]:
                    letra_colorida = " "
                else:
                    letra_colorida = f"{cor}{letra}{ENDC}"
                linha_colorida += letra_colorida
            linhas_de_teclas_coloridas.append(linha_colorida)
        return linhas_de_teclas_coloridas

    ###########################################################################
    ################                  GAME                 ####################
    ###########################################################################

    def print_game_at_pos(self, chutes, teclado_com_dicas, pos, feedbacks):
        print(self.tmanipulator.go_to_pos(pos), end="")
        sys.stdout.flush()
        self.print_keyboard(teclado_com_dicas)
        self.print_tabela(len(chutes))
        self.print_chutes(chutes, feedbacks)
        print(self.tmanipulator.go_to_pos((-pos[0], -pos[1])), end="")
        sys.stdout.flush()
        pass

    ###########################################################################
    ################               MENSAGENS               ####################
    ###########################################################################

    def message(self, mensagem):
        self.tmanipulator.clear_line(lim_chutes + 6)
        self.tmanipulator.print_at_pos(mensagem, (lim_chutes + 6, 0))

    def print_won_the_game(self, number_of_tries):
        self.message(f"\rParabéns! Você acertou em {number_of_tries} tentativas!")
        print(self.tmanipulator.go_to_pos((lim_chutes + 7, 0)))

    def print_loss_the_game(self, desafios):
        palavras_sorteadas = ""
        for d in desafios:
            palavras_sorteadas += " " + d.palavra
        self.message(f"\rVocê perdeu. As palavras eram{palavras_sorteadas}.")
        print(self.tmanipulator.go_to_pos((lim_chutes + 7, 0)))

    def print_word_not_accepted(self, palavra):
        self.message(f"Essa palavra não é aceita:{palavra}")

    def first_print(self):
        print("-------------O TERMO TERMINAL--------------")
        print("versão para terminal de https://www.term.ooo")
        # Limpa a tela
        s = ""
        for i in range(80):
            s += " "
        for i in range(lim_chutes + 7):
            print(s)
        print(f"\033[{lim_chutes + 7}A", end="")
        sys.stdout.flush()

        ###########################################################################
        ###########################################################################
        ################                                       ####################
        ################                INPUTS                 ####################
        ################                                       ####################
        ###########################################################################
        ###########################################################################

    ###########################
    def get_input(self, n, padding):
        pos = (0, padding)
        print(self.tmanipulator.go_to_pos(pos), end="")
        self.tmanipulator.clear_line(n + 1)
        self.print_tabela(n)
        s = self.tmanipulator.go_to_pos((n + 1, 2))
        chute_atual = unidecode(input(s)).upper()
        print(self.tmanipulator.go_to_line(-n - 2), end="")
        # print(self.tmanipulator.go_to_pos((-pos[0], -pos[1])), end="")
        sys.stdout.flush()
        return chute_atual


###########################################################################
###########################################################################
################                                       ####################
################                INÍCIO                 ####################
################                                       ####################
###########################################################################
###########################################################################


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
    tmanipulator = TerminalManipulator(None)
    presenter = TerminalPresenter(tmanipulator)

    presenter.first_print()

    ###########################################################################
    ################             MAIN LOOP                 ####################
    ###########################################################################
    padding = 4
    chute_atual = ""
    tentativas = 0
    spacing = 16
    while 1:
        # VISUALIZA
        for i in range(len(desafios)):
            teclado_linhas = desafios[i].teclado.get_keyboard_lines_with_hints()
            presenter.print_game_at_pos(
                desafios[i].chutes,
                teclado_linhas,
                (0, padding + i * spacing),
                desafios[i].feedbacks,
            )

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