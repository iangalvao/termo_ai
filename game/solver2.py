from solver_tools import WordFilter, HintList, Hint
import random
from word_checker import WordChecker


class Solver:
    def __init__(self, word_list) -> None:
        self.word_list = word_list
        self.possible_words = word_list.copy()
        self.word_filter = WordFilter()
        self.chutes = []
        self.feedbacks = []

    def reset(self):
        self.possible_words = self.word_list.copy()
        self.chutes = []
        self.feedbacks = []

    def generate_answer(self, feedbacks):
        self.feedbacks = feedbacks
        if len(self.chutes) == 0:
            res = "ricas"
        elif len(self.chutes) == 1:
            res = "nuvem"
        elif len(self.chutes) == 2:
            res = "ptdob"
        elif len(self.chutes) == 3:
            self.possible_words = self.word_filter.filter_from_feedback_list(
                self.chutes, feedbacks, self.possible_words
            )
            palavra, media = self.select_word_from_mean_filter_size(self.possible_words)
            res = palavra
        elif len(self.chutes) == 4:
            self.possible_words = self.word_filter.filter_from_feedback_list(
                self.chutes, feedbacks, self.possible_words
            )
            palavra, media = self.select_word_from_mean_filter_size(self.possible_words)
            res = palavra
        else:
            if len(self.possible_words) == 0:
                print("rand")
                word = self.random_word(self.word_list)
                res = word
            else:
                self.possible_words = self.word_filter.filter_from_feedback_list(
                    self.chutes, feedbacks, self.possible_words
                )
                word = self.random_word(self.possible_words)
                res = word

        self.chutes.append(res)
        return res

    def random_word(self, words):
        if len(words) == 0:
            s = ""
            for i in range(5):
                s += self.generate_random_char()
            return s
        random_number = random.randint(0, len(words) - 1)

        word = words[0]

        return word

    def mean_filter_size(self, word, possible_words, feedbacks, chutes, word_checker):
        summation = 0
        for pw in possible_words:

            feedback = word_checker.get_feedback_from_guess(word, pw)
            feedbacks.append(feedback)
            chutes.append(word)
            remaining_words_size = len(
                self.word_filter.filter_from_feedback_list(
                    chutes,
                    feedbacks,
                    possible_words,
                )
            )
            feedbacks.pop()
            chutes.pop()
            summation += remaining_words_size

        mean = summation / len(possible_words)

        return mean

    def select_word_from_mean_filter_size(self, possible_words):
        best_mean = 1000000
        best_word = self.word_list[0]
        chutes = [c for c in self.chutes]
        feedbacks = [f for f in self.feedbacks]
        word_checker = WordChecker()
        # só uma palavra certa
        if len(possible_words) == 1:
            return possible_words[0], 1
        if len(possible_words) < 50:
            for word in possible_words:
                mean = self.mean_filter_size(
                    word, possible_words, feedbacks, chutes, word_checker
                )
                if mean == 1:
                    print(word, mean)
                    return word, mean

        for word in self.word_list:
            mean = self.mean_filter_size(
                word, possible_words, feedbacks, chutes, word_checker
            )
            if mean == 1:
                print(word, mean)
                return word, mean
            if mean < best_mean:
                best_mean = mean
                best_word = word
        print(best_word, best_mean)
        return best_word, best_mean


from unidecode import unidecode
import csv


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


if __name__ == "__main__":
    n_desafios, lim_chutes, palavras_unidecode, palavras, solver, palavras_possiveis = (
        init_game()
    )
    palavra = "termo"
    wchecker = WordChecker()
    for i in range(len(palavras_possiveis)):
        palavra = unidecode(palavras_possiveis[i])
        feedbacks = []
        print("A palavra é", palavra)
        for i in range(6):
            guess = solver.generate_answer(feedbacks)
            print(guess)
            if guess != palavra:
                fb = wchecker.get_feedback_from_guess(guess, palavra)
                feedbacks.append(fb)
            else:
                print("Ganhou")
                break
        solver.reset()
