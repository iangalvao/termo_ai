from unidecode import unidecode
import csv
import random

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

COR_ERRADO = bcolors["FAIL"]
COR_CERTO = bcolors["OKGREEN"]
COR_POSICAO = bcolors["WARNING"]
ENDC = bcolors["ENDC"]

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


def count_letters_in_wrong_pos(palavra, chute, letra):
    c = count_letters(palavra, letra)
    w = letters_in_right_pos(palavra, chute, letra)
    return c - w


def count_letters(palavra, letra):
    res = 0
    for c in unidecode(palavra):
        if c == unidecode(letra):
            res += 1
    return res


def letters_in_right_pos(palavra1, palavra2, letra):
    c_count = 0
    letra = unidecode(letra)
    for i in range(len(palavra2)):
        c1 = unidecode(palavra1[i])
        c2 = unidecode(palavra2[i])
        if c1 == letra:
            if c2 == letra:
                c_count += 1
    return c_count


def check_word(chute):
    word = []

    for i in range(5):
        res = LETRA_INCORRETA
        if unidecode(chute[i]) == unidecode(palavra[i]):
            res = CERTO
        elif unidecode(chute[i]) in unidecode(palavra):
            if count_letters_in_wrong_pos(palavra, chute, chute[i]) >= count_letters(
                chute[: i + 1], chute[i]
            ):
                res = POS_INCORRETA
        word.append((chute[i], res))
    return word


def render_try(chute):
    vis = ""
    for i in range(5):
        cor = ENDC
        if chute[i][1] == CERTO:
            cor = COR_CERTO
        elif chute[i][1] == POS_INCORRETA:
            cor = COR_POSICAO
        vis += f"{cor}{chute[i][0]}{ENDC}"
    return vis


def print_tries(chutes):
    # get current tries string with embeded colors codes
    clean_last_line()
    print("\r", end="\033[7A")
    render_strings = []
    for chute in chutes:
        render_strings.append((render_try(chute)))

    # prepare the final strings, with 6 lines:
    final_string = ""
    prefix = "    "
    for i in range(6):
        if i < len(render_strings):
            final_string += prefix + render_strings[i]
        else:
            final_string += prefix
        if i < 5:
            final_string += "\n"
    print(
        final_string,
        end="\033[6A",
    )


def get_input():
    clean_line()
    chute_atual = unidecode(input("Seu chute: ")).upper()

    return chute_atual


def won_the_game(chute):
    if chute == palavra:
        return 1


def clean_line():
    s = ""
    for i in range(80):
        s += " "
    print(f"\r{s}", end="\r")


def clean_last_line():
    s = ""
    for i in range(6 + 1):
        s += "\n"
    for i in range(80):
        s += " "
    print(f"\r{s}", end="\r")


def clean_keyboard_area():
    s = ""
    for i in range(6 + 3):
        s += "\n"
    for i in range(3):
        for i in range(80):
            s += " "
        s += "\n"
    print(f"\r{s}", end="\033[3A")


def print_keyboard(chutes):
    keyboard_lines = get_keyboard_lines_with_hints(chutes)
    clean_keyboard_area()

    for i in range(len(keyboard_lines)):
        line = keyboard_lines[i]
        linha_colorida = ""
        for pack in line:
            letra = pack[0]
            dica = pack[1]
            cor = cores_das_dicas[dica]
            letra_colorida = f"{cor}{letra}{ENDC}"
            linha_colorida += letra_colorida

        print(f"\r{linha_colorida}")

    print("\r", end="\033[12A")


def get_keyboard_lines_with_hints(chutes):
    lines = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    lines_with_hints = [[], [], []]
    for i in range(len(lines)):
        line = lines[i]
        for c in line:
            hint = get_better_hint(c, chutes)
            lines_with_hints[i].append((c, hint))
    return lines_with_hints


def get_better_hint(c, chutes):
    hint = -1
    for chute in chutes:
        h = get_hint(c, chute)
        if h > hint:
            hint = h
    return hint


def get_hint(c, chute):
    res = -1
    for letra_e_dica in chute:
        letra = letra_e_dica[0]
        dica = letra_e_dica[1]
        if c == unidecode(letra):
            d = dica
            if d > res:
                res = d
    return res


# ABRE LISTA DE PALAVRAS E REMOVE ACENTUAÇÂO
with open("palavras.csv") as csvfile:
    myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
    palavras = next(myreader)
palavras_unidecode = {}
for palavra in palavras:
    palavras_unidecode[unidecode(palavra)] = palavra

# SORTEIO DA PALAVRA
random_number = random.randint(1, len(palavras))
palavra = palavras[random_number].upper()

# START
lim_chutes = 6
chutes = []
while 1:
    # INPUT
    print_keyboard(chutes)
    chute_atual = get_input()
    if chute_atual.lower() not in palavras_unidecode.keys():
        clean_last_line()
        print(
            f"\rEssa palavra não é aceita:{chute_atual}",
            end="\033[8A",
        )

        continue
    chute_atual = palavras_unidecode[chute_atual.lower()].upper()

    # CORRIGE
    chute_corrigido = check_word(chute_atual)
    chutes.append(chute_corrigido)
    # VISUALIZA
    print_tries(chutes)
    # GANHOU
    if won_the_game(chute_atual):
        clean_last_line()
        print(f"\rParabéns! Você venceu em {len(chutes)} tentativas!\n\n\n\n")
        exit(0)
    # PERDEU
    if len(chutes) == lim_chutes:
        clean_last_line()
        print(f"\rVocê perdeu. A palavra era {palavra}.\n\n\n\n")
        exit(0)
