from unidecode import unidecode
import csv
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


###########################################################################
################                                       ####################
################                LÓGICA                 ####################
################                                       ####################
###########################################################################


###########################################################################
################            CHECAGEM DE LETRAS         ####################
###########################################################################


def check_valid_word(palavra):
    return palavra.lower() not in palavras_unidecode.keys()


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
        for letra_e_dica in chute:
            letra = letra_e_dica[0]
            dica = letra_e_dica[1]
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
        self.state[letra] = dica

    def get_letter_hint(self, letra):
        return self.state[letra]


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


def go_to_line(n):
    s = ""
    for i in range(n):
        s += "\n"
    return s


def go_to_char(n):
    s = ""
    for i in range(n):
        s += " "
    return s


def go_to_pos(pos):
    s = go_to_line(pos[0])
    s += go_to_char(pos[1])
    return s


def print_at_pos(string, pos):
    s = go_to_pos(pos)
    s += string
    end = f"\033[{pos[0]}A\r"
    if pos[0] == 0:
        end = "\r"
    print(s, end=end)


def clean_line(n):
    s = ""
    for i in range(80):
        s += " "
    print_at_pos(s, (n, 0))


def clean_last_line():
    s = ""

    for i in range(80):
        s += " "
    print_at_pos(f"\r{s}", (10, 0))


###########################################################################
################           TELA PRINCIPAL              ####################
###########################################################################


################               CHUTES                  ####################
def colore_lista_chutes(chutes):
    chutes_coloridos = []
    for chute in chutes:
        chutes_colorido = ""
        for letra, dica in chute:
            cor = cores_das_dicas[dica]
            letra_colorida = f"{cor}{letra}{ENDC}"
            chutes_colorido += f"{cor}{letra_colorida}{ENDC}"
        chutes_coloridos.append(chutes_colorido)
    return chutes_coloridos


def print_chutes(chutes):
    chutes_coloridos = colore_lista_chutes(chutes)
    for i in range(len(chutes_coloridos)):
        print_at_pos(chutes_coloridos[i], (1 + i, 2))


#################                TECLADO                  ####################
def print_keyboard(linhas_teclado_dicas):
    linhas_teclas_coloridas = color_keyboard_lines(linhas_teclado_dicas)
    for i in range(3):
        linha_colorida = linhas_teclas_coloridas[i]
        if i == 2:  # A última linha começa uma casa depois por escolha de diagramação.
            linha_colorida = " " + linha_colorida
        print_at_pos(linhas_teclas_coloridas[i], (8 + i, 0))


def color_keyboard_lines(linhas_de_teclas_com_dicas):
    linhas_de_teclas_coloridas = []
    for linha in linhas_de_teclas_com_dicas:
        linha_colorida = ""
        for letra, dica in linha:
            cor = cores_das_dicas[dica]
            letra_colorida = f"{cor}{letra}{ENDC}"
            linha_colorida += letra_colorida
        linhas_de_teclas_coloridas.append(linha_colorida)
    return linhas_de_teclas_coloridas


###########################################################################
################               MENSAGENS               ####################
###########################################################################


def message(mensagem):
    print_at_pos(mensagem, (12, 0))


def print_won_the_game(number_of_tries):
    message(f"\rParabéns! Você acertou em {len(chutes)} tentativas!")


def print_loss_the_game(palavra):
    message(f"\rVocê perdeu. A palavra era {palavra}.")


def print_word_not_accepted(palavra):
    message(f"Essa palavra não é aceita:{chute_atual}")


def first_print():
    print("-------------O TERMO TERMINAL--------------")
    print("versão para terminal de https://www.term.ooo")
    s = ""
    for i in range(lim_chutes):
        s += "\n"
        print(
            s + "  " + UNDERLINE + "     " + END_UNDERLINE,
            end=f"\033[{i+1}A\r",
        )


###########################################################################
###########################################################################
################                                       ####################
################                INPUTS                 ####################
################                                       ####################
###########################################################################
###########################################################################


def get_input(n):
    clean_line(n + 1)
    print_at_pos(UNDERLINE + "     " + END_UNDERLINE, (n + 1, 2))
    s = go_to_pos((n + 1, 2))
    chute_atual = unidecode(input(s)).upper()
    print("\r", end=f"\033[{n+2}A")

    return chute_atual


###########################################################################
###########################################################################
################                                       ####################
################                INÍCIO                 ####################
################                                       ####################
###########################################################################
###########################################################################

# ABRE LISTA DE PALAVRAS E REMOVE ACENTUAÇÂO
with open("palavras.csv") as csvfile:
    myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
    palavras = next(myreader)
palavras_unidecode = {}
for palavra in palavras:
    palavras_unidecode[unidecode(palavra)] = palavra


# GAME INIT

# SORTEIO DA PALAVRA
random_number = random.randint(1, len(palavras) - 1 - 9147)
palavra = palavras[9147 + random_number].upper()

lim_chutes = 6

word_checker = Chutes()
keyboard = Keyboard()
chutes = []


first_print()

###########################################################################
################             MAIN LOOP                 ####################
###########################################################################

while 1:
    # INPUT
    keyboard_lines = keyboard.get_keyboard_lines_with_hints()
    print_keyboard(keyboard_lines)
    chute_atual = get_input(len(word_checker.chutes))
    if check_valid_word(chute_atual):
        print_word_not_accepted(chute_atual)
        continue
    chute_atual = palavras_unidecode[chute_atual.lower()].upper()

    # CORRIGE
    chute_corrigido = word_checker.update(palavra, chute_atual)
    keyboard.process_hints(chute_corrigido)
    # VISUALIZA
    print_chutes(word_checker.chutes)
    # GANHOU
    if won_the_game(chute_atual):
        print_won_the_game(len(word_checker.chutes))
        print(go_to_pos((13, 0)))
        exit(0)
    # PERDEU
    if len(word_checker.chutes) == lim_chutes:
        print_loss_the_game(palavra)
        print(go_to_pos((13, 0)))
        exit(0)
