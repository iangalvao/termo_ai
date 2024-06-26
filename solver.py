import random
import string
from game import Desafio, sort_words, won_the_game, check_valid_word

# Example usage


class Solver:
    def __init__(self, word_list) -> None:
        self.word_list = word_list

    def generate_answer(self, chutes, palavras):

        if len(palavras) == 0:

            # print(                "Random guess",            )
            word = self.random_word(self.word_list)
            return word, palavras
        else:
            palavras = self.get_letters_with_hints(chutes)
            word = self.random_word(palavras)
            return word, palavras

    def random_word(self, words):
        if len(words) == 0:
            s = ""
            for i in range(5):
                s += self.generate_random_char()
            return s
        random_number = random.randint(0, len(words) - 1)
        # print(f"Number:{random_number} Len:{len(words)}")

        word = words[random_number]

        return word

    def count_letters_in_list(self, word_list):
        count = {}
        for c in "qwertyuiopasdfghjklzxcvbnm":
            count[c] = 0
        for word in word_list:
            for c, n in self.count_letters(word):
                count[c] += n
        return count

    def get_letters_with_hints(self, hints):
        hints = self.get_best_hints(hints)
        palavras = self.word_list
        s = set()
        for c, hint_list in hints.items():
            for d, p in hint_list:

                if d == 1:
                    palavras = [
                        w for w in palavras if (c.lower() in w and w[p] != c.lower())
                    ]
                    s.add(c.lower())

                elif d == 0:
                    do = True
                    for dica, pos in hint_list:
                        if dica > 0:
                            do = False
                    if do:
                        palavras = [w for w in palavras if c.lower() not in w]

                elif d == 2:
                    palavras = [w for w in palavras if w[p] == c.lower()]
                    s.add(c.lower())
        return palavras

    def get_best_hints(self, chutes):
        res = {}
        for chute in chutes:
            pos = 0
            for c, d in chute:
                if c not in res.keys():
                    res[c] = [(d, pos)]
                else:
                    res[c].append((d, pos))
                pos += 1
        return res

    def generate_random_char(self):
        return random.choice(string.ascii_lowercase)


# ABRE LISTA DE PALAVRAS E REMOVE ACENTUAÇÂO
import csv
from unidecode import unidecode

data = [0, 0]


def won():
    data[0] += 1


def lose():
    data[1] += 1


def init_game():
    # Check if an argument is passed
    n_desafios = 1
    with open("palavras.csv") as csvfile:
        myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        palavras = next(myreader)
    palavras_unidecode = {}
    lista_unidecode = []
    for palavra in palavras:
        palavras_unidecode[unidecode(palavra)] = palavra
        lista_unidecode.append(unidecode(palavra))
    lim_chutes = 5 + n_desafios
    palavra_possiveis = list(palavras_unidecode.keys())[9147:]
    solver = Solver(palavra_possiveis)

    return n_desafios, lim_chutes, palavras_unidecode, palavras, solver
    # n_desafios = 2


def simulate(n_desafios, lim_chutes, palavras_unidecode, palavras, solver):
    desafios = []
    palavras = sort_words(list(palavras_unidecode.keys()), n_desafios)
    print("A Palavra é", palavras[0])
    for i in range(n_desafios):
        desafios.append(Desafio(palavras[i]))
    lista_chutes = palavras
    ###########################################################################
    ################             MAIN LOOP                 ####################
    ###########################################################################
    chute_atual = ""
    tentativas = 0
    while 1:
        # GANHOU
        if won_the_game(desafios):
            print("GANHOU")
            won()
            break
        # PERDEU
        if tentativas == lim_chutes:
            print("PERDEU")
            lose()
            break
        # INPUT
        chute_atual, lista_chutes = solver.generate_answer(
            desafios[i].chutes, lista_chutes
        )
        chute_atual = unidecode(chute_atual)
        if not check_valid_word(chute_atual, palavras_unidecode):
            continue
        chute_atual = chute_atual.lower().upper()
        print(f"CHUTE: {chute_atual}")
        tentativas += 1
        for i in range(len(desafios)):
            if not desafios[i].solved:
                chute_corrigido = desafios[i].update(chute_atual)
                desafios[i].teclado.process_hints(chute_corrigido)


n_desafios, lim_chutes, palavras_unidecode, palavras, solver = init_game()
for i in range(3000):
    simulate(n_desafios, lim_chutes, palavras_unidecode, palavras, solver)
    print(i, data)
print(data)
