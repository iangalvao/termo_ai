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
    def __init__(self, palavra) -> None:
        self.chutes = []
        self.teclado = Keyboard()
        self.palavra = palavra
        self.solved = 0

    def count_letters_in_wrong_pos(self, chute, letra):
        c = self.count_letters(self.palavra, letra)
        w = self.letters_in_right_pos(self.palavra, chute, letra)
        return c - w

    def count_letters(self, chute, letra):
        res = 0
        for c in unidecode(chute):
            if unidecode(c) == unidecode(letra):
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

    def check_word(self, chute):
        word = []

        for i in range(5):
            dica = LETRA_INCORRETA
            if unidecode(chute[i]) == unidecode(self.palavra[i]):
                dica = CERTO
            elif unidecode(chute[i]) in unidecode(self.palavra):
                if self.count_letters_in_wrong_pos(
                    chute, chute[i]
                ) + self.letters_in_right_pos(
                    self.palavra[: i + 1], chute[: i + 1], chute[i]
                ) >= self.count_letters(
                    chute[: i + 1], chute[i]
                ):
                    dica = POS_INCORRETA
            word.append((chute[i], dica))

        return word

    def update(self, chute):
        if chute == self.palavra:
            self.solved = 1
        chute_corrigido = self.check_word(chute)
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
        for i in range(lim_chutes - n):
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
            if i == 2:
                # A última linha começa uma casa depois por escolha de diagramação.
                linha_colorida = " " + linha_colorida
            self.print_at_pos(linhas_teclas_coloridas[i], (lim_chutes + 2 + i, 0))

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
        self.clean_line(lim_chutes + 6)
        self.print_at_pos(mensagem, (lim_chutes + 6, 0))

    def print_won_the_game(self, number_of_tries):
        self.message(f"\rParabéns! Você acertou em {number_of_tries} tentativas!")
        print(self.go_to_pos((lim_chutes + 7, 0)))

    def print_loss_the_game(self, desafios):
        palavras_sorteadas = ""
        for d in desafios:
            palavras_sorteadas += " " + d.palavra
        self.message(f"\rVocê perdeu. As palavras eram{palavras_sorteadas}.")
        print(self.go_to_pos((lim_chutes + 7, 0)))

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

    desafios = []
    palavras = sort_words(palavras, n_desafios)
    for i in range(n_desafios):
        desafios.append(Desafio(palavras[i]))

    presenter = TerminalPresenter()

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
                desafios[i].chutes, teclado_linhas, (0, padding + i * spacing)
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
        presenter.clean_line(12)  # Apaga mensagens.

        # CORRIGE
        for i in range(len(desafios)):
            if not desafios[i].solved:
                chute_corrigido = desafios[i].update(chute_atual)
                desafios[i].teclado.process_hints(chute_corrigido)
