import copy
import csv
from typing import List

from unidecode import unidecode

from game.model.attempt import Attempt
from game.model.hint import RIGHT_POS, WRONG_LETTER, WRONG_POS, Hint
from game.solver.solver_tools import WordFilter


class Solver:
    def __init__(
        self, possible_guesses: List[str], tests: List[str], word_filter: WordFilter
    ) -> None:
        self.possible_guesses: List[str] = possible_guesses
        self.tests: List[str] = tests
        self.aux_list1 = ["" for _ in range(len(possible_guesses))]
        self.aux_list2 = ["" for _ in range(len(possible_guesses))]
        self.feedbacks = []
        self.word_filter = word_filter

    def generate_answer(self, feedbacks: List[Hint]):
        if len(self.tests) == 0:
            raise RuntimeError(
                "Empty possible test words on Solver. No possible solution can be found."
            )

        self.feedbacks = feedbacks
        # self.tests = self.word_filter.filter_from_feedback_list(
        #    self.chutes, feedbacks, self.tests
        # )
        result = {}
        dict_template = {}
        for i in range(243):
            f4 = str(i % 3)
            f3 = str(i % 9 // 3)
            f2 = str(i % 27 // 9)
            f1 = str(i % 81 // 27)
            f0 = str(i // 81)

            key = f0 + f1 + f2 + f3 + f4
            # dict_template[key] = []
            dict_template[key] = 0
        i = 0
        for guess in self.possible_guesses:
            # word_result = copy.deepcopy(dict_template)
            word_result = dict_template.copy()
            for word in self.tests:
                attempt = Attempt(guess, word)
                key = self.feedback_to_key(attempt.feedbacks)
                # word_result[key].append(word)
                word_result[key] += 1

            result[guess] = word_result
            print(guess, i)
            i += 1
            s = 0
            m = 0
            c = 0
            for value in word_result.values():
                if value > 0:
                    s += value
                    if value > m:
                        m = value
                    c += 1
            s = s / c
            print(s, m)
        return result

    def feedback_to_key(self, fb):
        if len(fb) == 0:
            return None
        s = ""
        for i in fb:
            if i == RIGHT_POS:
                s += "2"
            elif i == WRONG_POS:
                s += "1"
            elif i == WRONG_LETTER:
                s += "0"
        return s


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

    # lista_unidecode = ["arara", "arame", "morno", "azedo", "amado", "ximbo", "pizza"]
    # palavra_possiveis = ["morno", "azedo", "amado", "ximbo", "pizza"]
    lista_unidecode = palavra_possiveis
    return (
        n_desafios,
        lim_chutes,
        lista_unidecode,
        palavra_possiveis,
    )


if __name__ == "__main__":
    n_desafios, lim_chutes, palavras_unidecode, palavras_possiveis = init_game()
    word_filter = WordFilter()
    solver = Solver(palavras_unidecode, palavras_possiveis, word_filter)
    for i in range(len(palavras_possiveis)):
        feedbacks = []
        palavra = palavras_possiveis[i]
    results = solver.generate_answer(feedbacks)
    for key, value in results.items():
        print(key)
        s = 0
        m = 0
        c = 0
        for fb, words in value.items():
            if words > 0:
                s += words
                if words > m:
                    m = words
                c += 1
        s = s / c
        print(s, m)
