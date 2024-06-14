from unidecode import unidecode
import csv
import sys
import random
from colorama import Fore, Back, Style


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
    LETRA_DESCONHECIDA: ENDC,
    LETRA_INCORRETA: COR_ERRADO,
    POS_INCORRETA: COR_POSICAO,
    CERTO: COR_CERTO,
}


###########################################################################
################                                       ####################
################                 JOGO                  ####################
################                                       ####################
###########################################################################


def won_the_game(chute):
    if chute == palavra:
        return 1


def check_valid_word(palavra):
    return palavra.lower() not in palavras_unidecode.keys()


###########################################################################
################                                       ####################
################                LÓGICA                 ####################
################                                       ####################
###########################################################################


###########################################################################
################            CHECAGEM DE LETRAS         ####################
###########################################################################


class Chutes:
    def __init__(self) -> None:
        self.chutes = []

    def count_letters_in_wrong_pos(self, palavra, chute, letra):
        c = self.count_letters(palavra, letra)
        w = self.letters_in_right_pos(palavra, chute, letra)
        return c - w

    def count_letters(self, palavra, letra):
        res = 0
        for c in unidecode(palavra):
            if c == unidecode(letra):
                res += 1
        return res

    def letters_in_right_pos(self, palavra1, palavra2, letra):
        c_count = 0
        letra = unidecode(letra)
        for i in range(len(palavra2)):
            c1 = unidecode(palavra1[i])
            c2 = unidecode(palavra2[i])
            if c1 == letra:
                if c2 == letra:
                    c_count += 1
        return c_count

    def check_word(self, palavra, chute):
        word = []

        for i in range(5):
            res = LETRA_INCORRETA
            if unidecode(chute[i]) == unidecode(palavra[i]):
                res = CERTO
            elif unidecode(chute[i]) in unidecode(palavra):
                if self.count_letters_in_wrong_pos(
                    palavra, chute, chute[i]
                ) + self.letters_in_right_pos(
                    palavra[: i + 1], chute[: i + 1], chute[i]
                ) >= self.count_letters(
                    chute[: i + 1], chute[i]
                ):
                    res = POS_INCORRETA
            word.append((chute[i], res))
        return word

    def update(self, palavra, chute):
        chute_corrigido = self.check_word(palavra, chute)
        self.chutes.append(chute_corrigido)
        return chute_corrigido


###########################################################################
################                 TECLADO               ####################
###########################################################################


class Keyboard:
    def __init__(self) -> None:
        self.lines = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        self.state = {}
        for line in self.lines:
            for c in line:
                self.set_letter_hint(c, LETRA_DESCONHECIDA)

    def process_hints(self, chute):
        for letra, dica in chute:
            dica_atual = self.get_letter_hint(letra)
            if dica > dica_atual:
                self.set_letter_hint(letra, dica)

    def get_keyboard_lines_with_hints(self):
        res = []
        for linha in self.lines:
            linha_com_dicas = []
            for letra in linha:
                linha_com_dicas.append((letra, self.get_letter_hint(letra)))
            res.append(linha_com_dicas)
        return res

    def set_letter_hint(self, letra, dica):
        self.state[unidecode(letra)] = dica

    def get_letter_hint(self, letra):
        return self.state[unidecode(letra)]


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
    def __init__(self) -> None:

        pass

    def go_to_line(self, n):
        if n == 0:
            return ""
        elif n > 0:
            return f"\033[{n}B"
        else:
            return f"\033[{-n}A"

    def go_to_char(self, n):
        if n == 0:
            return ""
        elif n > 0:
            return f"\033[{n}C"
        else:
            return f"\033[{-n}D"

    def go_to_pos(self, pos):
        return self.go_to_line(pos[0]) + self.go_to_char(pos[1])

    def tamanho_string(self, s):
        count = 0
        n = 0
        for i in range(len(s)):
            if i + n >= len(s):
                break
            c = s[i + n]
            if c == "\033":
                while len(s) > i + n:
                    n += 1
                    c = s[i + n]
                    if c.isalpha():
                        break
                continue
            # print("c:", c)
            if c.isalnum() or c == " " or c == ":":
                count += 1
        return count

    def print_at_pos(self, s, pos):
        padding = self.go_to_pos(pos)
        end_v = self.go_to_line(-pos[0])
        end_h = self.go_to_char(-(pos[1] + self.tamanho_string(s)))
        end = end_v + end_h
        print(padding + s, end=end)
        sys.stdout.flush()

    def clean_line(self, n):
        s = ""
        for i in range(80):
            s += " "
        self.print_at_pos(s, (n, 0))

    ###########################################################################
    ################           TELA PRINCIPAL              ####################
    ###########################################################################

    ################               CHUTES                  ####################

    def print_tabela(self, n):
        for i in range(6 - n):
            self.print_at_pos(UNDERLINE + "     " + END_UNDERLINE, (i + n + 1, 2))

    def print_chutes(self, chutes):
        chutes_coloridos = self.colore_lista_chutes(chutes)
        for i in range(len(chutes_coloridos)):
            self.print_at_pos(chutes_coloridos[i], (i + 1, 2))

    def colore_lista_chutes(self, chutes):
        chutes_coloridos = []
        for chute in chutes:
            chutes_colorido = ""
            for letra, dica in chute:
                if dica == LETRA_INCORRETA:
                    dica = LETRA_DESCONHECIDA
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
            if (
                i == 2
            ):  # A última linha começa uma casa depois por escolha de diagramação.
                linha_colorida = " " + linha_colorida
            self.print_at_pos(linhas_teclas_coloridas[i], (8 + i, 0))

    def color_keyboard_lines(self, linhas_de_teclas_com_dicas):
        linhas_de_teclas_coloridas = []
        for linha in linhas_de_teclas_com_dicas:
            linha_colorida = ""
            for letra, dica in linha:
                cor = cores_das_dicas[dica]
                letra_colorida = f"{cor}{letra}{ENDC}"
                linha_colorida += letra_colorida
            linhas_de_teclas_coloridas.append(linha_colorida)
        return linhas_de_teclas_coloridas

    def print_game_at_pos(self, chutes, teclado_com_dicas, pos):
        print(self.go_to_pos(pos), end="")
        sys.stdout.flush()
        self.print_keyboard(teclado_com_dicas)
        self.print_tabela(len(chutes))
        self.print_chutes(chutes)
        print(self.go_to_pos((-pos[0], -pos[1])), end="")
        sys.stdout.flush()
        pass

    ###########################################################################
    ################               MENSAGENS               ####################
    ###########################################################################

    def message(self, mensagem):
        self.clean_line(12)
        self.print_at_pos(mensagem, (12, 0))

    def print_won_the_game(self, number_of_tries):
        self.message(f"\rParabéns! Você acertou em {number_of_tries} tentativas!")
        print(self.go_to_pos((13, 0)))

    def print_loss_the_game(self, palavra):
        self.message(f"\rVocê perdeu. A palavra era {palavra}.")
        print(self.go_to_pos((13, 0)))

    def print_word_not_accepted(self, palavra):
        self.message(f"Essa palavra não é aceita:{palavra}")

    def first_print(self):
        print("-------------O TERMO TERMINAL--------------")
        print("versão para terminal de https://www.term.ooo")

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
        print(self.go_to_pos(pos), end="")
        self.clean_line(n + 1)
        self.print_tabela(n)
        s = self.go_to_pos((n + 1, 2))
        chute_atual = unidecode(input(s)).upper()
        print(self.go_to_line(-n - 2), end="")
        # print(self.go_to_pos((-pos[0], -pos[1])), end="")
        sys.stdout.flush()
        return chute_atual


###########################################################################
###########################################################################
################                                       ####################
################                INÍCIO                 ####################
################                                       ####################
###########################################################################
###########################################################################

# ABRE LISTA DE PALAVRAS E REMOVE ACENTUAÇÂO

if __name__ == "__main__":
    with open("palavras.csv") as csvfile:
        myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        palavras = next(myreader)
    palavras_unidecode = {}
    for palavra in palavras:
        palavras_unidecode[unidecode(palavra)] = palavra

    # SORTEIO DA PALAVRA
    random_number = random.randint(1, len(palavras) - 1 - 9147)
    palavra = palavras[9147 + random_number].upper()
    random_number = random.randint(1, len(palavras) - 1 - 9147)
    palavra2 = palavras[9147 + random_number].upper()
    lim_chutes = 6

    word_checker = Chutes()
    desafio2_chutes = Chutes()
    keyboard = Keyboard()
    desafio2_teclado = Keyboard()

    presenter = TerminalPresenter()

    presenter.first_print()

    ###########################################################################
    ################             MAIN LOOP                 ####################
    ###########################################################################
    padding = 4
    chute_atual = ""
    while 1:
        # INPUT
        keyboard_lines = keyboard.get_keyboard_lines_with_hints()

        presenter.print_game_at_pos(word_checker.chutes, keyboard_lines, (0, padding))

        # desafio2_teclado_linhas = desafio2_teclado.get_keyboard_lines_with_hints()
        # presenter.print_game_at_pos(desafio2_chutes.chutes, desafio2_teclado_linhas, (0, padding + 16))
        if won_the_game(chute_atual):
            presenter.print_won_the_game(len(word_checker.chutes))
            exit(0)
        chute_atual = presenter.get_input(len(word_checker.chutes), padding)
        if check_valid_word(chute_atual):
            presenter.print_word_not_accepted(chute_atual)
            continue

        presenter.clean_line(12)  # Apaga mensagens.
        chute_atual = palavras_unidecode[chute_atual.lower()].upper()

        # CORRIGE
        chute_corrigido = word_checker.update(palavra, chute_atual)
        keyboard.process_hints(chute_corrigido)

        # chute_corrigido2 = desafio2_chutes.update(palavra2, chute_atual)
        # desafio2_teclado.process_hints(chute_corrigido2)
        # VISUALIZA
        # presenter.print_chutes(word_checker.chutes)
        # GANHOU

        # PERDEU
        if len(word_checker.chutes) == lim_chutes:
            presenter.print_loss_the_game(palavra)
            exit(0)
