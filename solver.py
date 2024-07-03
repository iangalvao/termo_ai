import random
import string
from game import Desafio, sort_words, won_the_game, check_valid_word
import csv
from unidecode import unidecode


# Example usage

# CÒDIGOS PARA CORREÇÂO DE CADA LETRA
LETRA_DESCONHECIDA = -1
LETRA_INCORRETA = 0
POS_INCORRETA = 1
CERTO = 2


################################################################################
################################################################################
################################################################################
#####                                                                      #####
#####                                                                      #####
#####                                Solver                                #####
#####                                                                      #####
#####                                                                      #####
################################################################################
################################################################################
################################################################################


class Solver:
    def __init__(self, word_list) -> None:
        self.word_list = word_list

    def generate_answer(self, chutes, palavras):
        if len(chutes) == 0:
            return "ricas", palavras
        if len(chutes) == 1:
            return "nuvem", palavras
        if len(chutes) == 2:
            return "ptdob", palavras
        if len(chutes) == 3:
            palavras = self.filter_from_hints(chutes, palavras)
            palavra, media = self.select_word_from_mean_filter_size(palavras)
            return palavra, palavras
        if len(chutes) == 4:
            palavras = self.filter_from_hints(chutes, palavras)
            palavra, media = self.select_word_from_mean_filter_size(palavras)
            return palavra, palavras
        if len(palavras) == 0:
            word = self.random_word(self.word_list)
            return word, palavras
        else:
            palavras = self.filter_from_hints(chutes, palavras)
            word = self.random_word(palavras)
            return word, palavras

    def random_word(self, words):
        if len(words) == 0:
            s = ""
            for i in range(5):
                s += self.generate_random_char()
            return s
        random_number = random.randint(0, len(words) - 1)

        word = words[0]

        return word

    def count_letters_in_list(self, word_list):
        count = {}
        for c in "qwertyuiopasdfghjklzxcvbnm":
            count[c] = 0
        for word in word_list:
            for c, n in self.count_letters(word):
                count[c] += n
        return count

    def filter_from_hints(self, hints, palavras: list):
        hint_list = self.get_all_hints(hints)
        palavras = palavras.copy()

        for c, hint_dict in hint_list.hints.items():
            for hint, value_set in hint_dict.items():
                for val in value_set:
                    if hint == 1:
                        palavras = [
                            w
                            for w in palavras
                            if (c.lower() in w and w[val] != c.lower())
                        ]

                    elif hint == 0:
                        palavras = [w for w in palavras if c.lower() not in w]

                    elif hint == 2:
                        palavras = [w for w in palavras if w[val] == c.lower()]

                    elif hint == 3:
                        palavras = [
                            w
                            for w in palavras
                            if len([l for l in w if l == c.lower()]) >= val
                        ]
        return palavras

    def get_hints(self, chute):
        hints = HintList()
        pos = 0
        number_of_letters = {}
        for c, d in chute:
            if d == 2:
                if c not in number_of_letters.keys():
                    number_of_letters[c] = 0
                number_of_letters[c] += 1
                hints.add(c, d, pos)
            elif d == 1:
                if c not in number_of_letters.keys():
                    number_of_letters[c] = 0
                number_of_letters[c] += 1
                hints.add(c, d, pos)
            elif d == 0:
                do = True
                for letra, dica in chute:
                    if letra.lower() == c.lower():
                        if dica > 0:
                            do = False
                if do:
                    hints.add(c, d, 0)
                else:
                    hints.add(c, 1, pos)
            pos += 1
        for c in number_of_letters.keys():
            hints.add(c, 3, number_of_letters[c])
        return hints

    def get_all_hints(self, chutes):
        all_hints = HintList()
        for chute in chutes:
            all_hints.merge(self.get_hints(chute))
        return all_hints

    def generate_random_char(self):
        return random.choice(string.ascii_lowercase)

    def mean_filter_size(self, word, possible_words):
        summation = 0
        for pw in possible_words:
            desafio = Desafio(pw)
            hints = [desafio.check_word(word)]
            remaining_words_size = len(
                self.filter_from_hints(
                    hints,
                    possible_words,
                )
            )
            summation += remaining_words_size

        mean = summation / len(possible_words)

        return mean

    def select_word_from_mean_filter_size(self, possible_words):
        best_mean = 1000000
        best_word = self.word_list[0]
        # só uma palavra certa
        if len(possible_words) == 1:
            return possible_words[0], 1
        for word in self.word_list:
            mean = self.mean_filter_size(word, possible_words)
            if mean == 1:
                print(word, mean)
                return word, mean
            if mean < best_mean:
                best_mean = mean
                best_word = word
        print(best_word, best_mean)
        return best_word, best_mean


################################################################################
################################################################################
################################################################################
#####                                                                      #####
#####                                                                      #####
#####                           Hints and Checks                           #####
#####                                                                      #####
#####                                                                      #####
################################################################################
################################################################################
################################################################################


class WordChecker:
    def __init__(self, word):
        self.word = word

    def filter_from_hint_list(self, hints, palavras: list):
        hint_list = self.get_all_hints(hints)
        palavras = palavras.copy()

        for c, char_hint_dict in hint_list.hints.items():
            for hint, value_set in char_hint_dict.items():
                for val in value_set:
                    palavras = self.filter_from_hint(self, hint, c, val, palavras)

    def filter_from_hint(self, hint, c, val, palavras):
        if hint == 1:
            palavras = [w for w in palavras if (c.lower() in w and w[val] != c.lower())]

        elif hint == 0:
            palavras = [w for w in palavras if c.lower() not in w]

        elif hint == 2:
            palavras = [w for w in palavras if w[val] == c.lower()]

        elif hint == 3:
            palavras = [
                w for w in palavras if len([l for l in w if l == c.lower()]) >= val
            ]
        return palavras

    def get_hints(self, chute):
        hints = HintList()
        pos = 0
        number_of_letters = {}
        for c, d in chute:
            if d == 2:
                if c not in number_of_letters.keys():
                    number_of_letters[c] = 0
                number_of_letters[c] += 1
                hints.add(c, d, pos)
            elif d == 1:
                if c not in number_of_letters.keys():
                    number_of_letters[c] = 0
                number_of_letters[c] += 1
                hints.add(c, d, pos)
            elif d == 0:
                do = True
                for letra, dica in chute:
                    if letra.lower() == c.lower():
                        if dica > 0:
                            do = False
                if do:
                    hints.add(c, d, 0)
                else:
                    hints.add(c, 1, pos)
            pos += 1
        for c in number_of_letters.keys():
            hints.add(c, 3, number_of_letters[c])
        return hints

    def get_all_hints(self, chutes):
        all_hints = HintList()
        for chute in chutes:
            all_hints.merge(self.get_hints(chute))
        return all_hints


class HintList:
    def __init__(self) -> None:
        self.hints = {}

    def add(self, c, hint, val):
        if c not in self.hints.keys():
            self.hints[c] = {}
        if hint not in self.hints[c].keys():
            self.hints[c][hint] = set()

        self.hints[c][hint].add(val)

    def merge(self, other):
        for c, hint_dict in other.hints.items():
            for hint, value_set in hint_dict.items():
                for val in value_set:
                    self.add(c, hint, val)


################################################################################
################################################################################
################################################################################
#####                                                                      #####
#####                                                                      #####
#####                           Experiment Setup                           #####
#####                                                                      #####
#####                                                                      #####
################################################################################
################################################################################
################################################################################


def init_game():
    # Check if an argument is passed
    n_desafios = 1
    with open("palavras.csv") as csvfile:
        myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        palavras_originais = next(myreader)
    palavras_unidecode = {}
    lista_unidecode = []
    for palavra in palavras_originais:
        palavras_unidecode[unidecode(palavra)] = palavra
        lista_unidecode.append(unidecode(palavra))
    lim_chutes = 5 + n_desafios
    palavra_possiveis = list(palavras_unidecode.keys())[9147:]
    solver = Solver(lista_unidecode)

    return (
        n_desafios,
        lim_chutes,
        palavras_unidecode,
        palavras_originais,
        solver,
        palavra_possiveis,
    )


def simulate(
    n_desafios, lim_chutes, palavras_unidecode, palavras, solver, target_words=None
):
    # Setup da simulação
    if target_words:
        palavras = target_words
    else:
        palavras = sort_words(list(palavras_unidecode.keys()), n_desafios)
    for i in range(len(palavras)):
        palavra = palavras[i]
        print(f"A {i}ª palavra é:", palavra)

    # Setup do Jogo
    desafios = []
    for i in range(n_desafios):
        desafios.append(Desafio(palavras[i]))
    lista_chutes = palavras_unidecode
    chute_atual = ""
    tentativas = 0

    ###########################################################################
    ################             MAIN LOOP                 ####################
    ###########################################################################

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


def won():
    data[0] += 1


def lose():
    data[1] += 1


n_desafios, lim_chutes, palavras_unidecode, palavras, solver, palavras_possiveis = (
    init_game()
)
data = [0, 0]
for i in range(len(palavras_possiveis)):
    target_words = [unidecode(palavras_possiveis[i]).upper()]
    simulate(
        n_desafios,
        lim_chutes,
        palavras_unidecode,
        palavras,
        solver,
        target_words=target_words,
    )
    print(i, data)
print(data)
