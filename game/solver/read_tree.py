from game.model.attempt import Attempt
from game.solver.tree import *


def init_game():
    # Check if an argument is passed
    with open("palavras.csv") as csvfile:
        myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        palavras_originais = next(myreader)
    palavras_unidecode = {}
    lista_unidecode = []
    for palavra in palavras_originais:
        palavras_unidecode[unidecode(palavra)] = palavra
        lista_unidecode.append(unidecode(palavra))

    palavra_possiveis = list(palavras_unidecode.keys())[9147:]

    return (
        lista_unidecode,
        palavra_possiveis,
    )


tb = TreeBuilder([])
f = open("game/resultados/solver3_tree3_termo.txt", "r")
tree = tb.read_from_string(f, 0)
tree.print_nodes_and_keys_padding("      ")

chutes_possiveis, palavras_termo = init_game()
resultados = [0 for i in range(10)]
for w in palavras_termo:
    feedbacks = []
    guess = ""
    n = 0
    while guess != w:
        guess = tree.generate_answer(feedbacks)
        feedback = Attempt(guess, w).feedbacks
        feedbacks.append(feedback)
        n += 1
        # print(guess)

    # print(f"Ganhou em {n} tentativas!")
    resultados[n - 1] += 1
# print(resultados)
