import random
import string
from game import Desafio, sort_words, won_the_game, check_valid_word

# Example usage

# CÒDIGOS PARA CORREÇÂO DE CADA LETRA
LETRA_DESCONHECIDA = -1
LETRA_INCORRETA = 0
POS_INCORRETA = 1
CERTO = 2


class DesafioS:
    def __init__(self, palavra) -> None:
        self.chutes = []
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

        return [word]


class Solver:
    def __init__(self, word_list) -> None:
        self.word_list = word_list

    def generate_answer(self, chutes, palavras):
        if len(chutes) == 0:
            return "pacto", palavras
        if len(chutes) == 1:
            return "mugir", palavras
        if len(chutes) == 2:
            return "bolas", palavras
        if len(chutes) == 3:
            return "fenda", palavras
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
                    if letra == c:
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

        i = 0
        for pw in possible_words:
            desafio = DesafioS(pw)
            hints = desafio.check_word(word)
            remaining_words_size = len(
                self.filter_from_hints(
                    hints,
                    possible_words,
                )
            )  # change filter_from_hints to receive original list and dont change it

            i += 1
            summation += remaining_words_size

        mean = summation / len(possible_words)
        return mean

    def select_word_from_mean_filter_size(self, possible_words):
        best_mean = 1000000
        best_word = self.word_list[0]
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
    solver = Solver(lista_unidecode)

    return n_desafios, lim_chutes, palavras_unidecode, palavras, solver
    # n_desafios = 2


def simulate(n_desafios, lim_chutes, palavras_unidecode, palavras, solver):
    desafios = []
    palavras = sort_words(list(palavras_unidecode.keys()), n_desafios)
    print("A Palavra é", palavras[0])
    for i in range(n_desafios):
        desafios.append(Desafio(palavras[i]))
    lista_chutes = palavras_unidecode
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
