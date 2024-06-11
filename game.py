import csv

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

with open("poucas_palavras.csv") as csvfile:
    myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
    palavras = next(myreader)

print(palavras)


cor_certo = "OKBLUE"
cor_posicao = "HEADER"
palavra = palavras[3].upper()

chute1 = "TRUPE"
chute2 = "TERNO"
chute3 = "TERMO"

chutes = [chute1, chute2, chute3]


def show_result(chute):
    vis = ""

    for i in range(5):
        if chute[i] == palavra[i]:
            cor = cor_certo
        elif chute[i] in palavra:
            cor = cor_posicao
        else:
            cor = "ENDC"
        vis += f"{bcolors[cor]}{chute[i]}{bcolors['ENDC']}"
    print(vis)
    if chute == palavra:
        return 1
    return 0


lim_chutes = 6
chutes = []
for chute in range(lim_chutes):
    a = input("Seu chute: ").upper()
    if a.lower() in palavras:
        chutes.append(a)
        for chute in chutes:
            r = show_result(chute)
            if r:
                print("Você venceu!")
                exit(0)
    else:
        print("Essa palavra não é aceita")
