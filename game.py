from unidecode import unidecode
import csv
import random

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

COR_CERTO = bcolors["OKGREEN"]
COR_POSICAO = bcolors["WARNING"]
ENDC = bcolors["ENDC"]


for name, color in bcolors.items():
    print(f"{color}{name}{ENDC}")


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


LETRA_INCORRETA = 0
POS_INCORRETA = 1
CERTO = 2


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


def show_result(chute):
    vis = ""
    for i in range(5):
        cor = ENDC
        if chute[i][1] == CERTO:
            cor = COR_CERTO
        elif chute[i][1] == POS_INCORRETA:
            cor = COR_POSICAO
        vis += f"{cor}{chute[i][0]}{ENDC}"
    print(vis)


def print_tries(chutes):
    for chute in chutes:
        show_result(chute)


def get_input():
    chute_atual = unidecode(input("Seu chute: ")).upper()
    if chute_atual.lower() not in palavras_unidecode.keys():
        return None
    return palavras_unidecode[chute_atual.lower()].upper()


def won_the_game(chute):
    if chute == palavra:
        return 1


with open("palavras.csv") as csvfile:
    myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
    palavras = next(myreader)

palavras_unidecode = {}
for palavra in palavras:
    palavras_unidecode[unidecode(palavra)] = palavra


random_number = random.randint(1, len(palavras))
palavra = palavras[random_number].upper()

lim_chutes = 6
chutes = []
while 1:
    chute_atual = get_input()
    if not chute_atual:
        print("Essa palavra não é aceita")

    chute_corrigido = check_word(chute_atual)
    chutes.append(chute_corrigido)
    print_tries(chutes)
    if won_the_game(chute_atual):
        print("Você venceu!")
        exit(0)
    if len(chutes) == lim_chutes:
        print(f"Você perdeu. A palavra era {palavra}.")
        exit(0)
