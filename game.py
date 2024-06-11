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

COR_CERTO = bcolors["OKBLUE"]
COR_POSICAO = bcolors["HEADER"]
ENDC = bcolors["ENDC"]


def count_letters_in_wrong_pos(palavra, chute, letra):
    c = count_letters(palavra, letra)
    w = letters_in_right_pos(palavra, chute, letra)
    return c - w


def count_letters(palavra, letra):
    res = 0
    for c in palavra:
        if c == letra:
            res += 1
    return res


def letters_in_right_pos(palavra1, palavra2, letra):
    c_count = 0
    for i in range(len(palavra2)):
        c1 = palavra1[i]
        c2 = palavra2[i]
        if c1 == letra:
            if c2 == letra:
                c_count += 1
    return c_count


def show_result(chute):
    vis = ""

    for i in range(5):
        cor = ENDC
        if chute[i] == palavra[i]:
            cor = COR_CERTO
        elif chute[i] in palavra:
            if count_letters_in_wrong_pos(palavra, chute, chute[i]) >= count_letters(
                chute[: i + 1], chute[i]
            ):
                cor = COR_POSICAO

        vis += f"{cor}{chute[i]}{ENDC}"
    print(vis)


with open("palavras.csv") as csvfile:
    myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
    palavras = next(myreader)

random_number = 3  # random.randint(1, len(palavras))
palavra = palavras[random_number].upper()

lim_chutes = 6
chutes = []
while 1:
    chute_atual = input("Seu chute: ").upper()
    if chute_atual.lower() not in palavras:
        print("Essa palavra não é aceita")
        continue
    chutes.append(chute_atual)
    for chute in chutes:
        show_result(chute)
    if chute_atual == palavra:
        print("Você venceu!")
        exit(0)
    if len(chutes) == lim_chutes:
        print(f"Você perdeu. A palavra era {palavra}.")
        exit(0)
