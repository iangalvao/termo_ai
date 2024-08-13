import datetime
import time
from game.solver.solver_tools import WordFilter, HintList
from game.model.hint import *
import random
from game.solver.word_checker import WordChecker


class Solver:
    def __init__(self, word_list, possible_words=None) -> None:
        self.word_list = word_list
        if possible_words:
            self.original_possible_words = possible_words
        else:
            self.original_possible_words = word_list.copy()
        self.possible_words = self.original_possible_words
        self.word_filter = WordFilter()
        self.chutes = []
        self.feedbacks = []

    def reset(self):
        self.possible_words = self.original_possible_words.copy()
        self.chutes = []
        self.feedbacks = []

    def generate_answer(self, feedbacks):
        if len(self.possible_words) == 0:
            raise RuntimeError("Empty possible words on Solver.")

        self.feedbacks = feedbacks
        self.possible_words = self.word_filter.filter_from_feedback_list(
            self.chutes, feedbacks, self.possible_words
        )
        if len(self.chutes) == 0:
            res = "pcdob"
        elif len(self.chutes) == 1:
            # palavra, media = self.select_word_from_mean_filter_size(self.possible_words)
            # res = palavra
            res = "flush"

        elif len(self.chutes) == 2:
            # palavra, media = self.select_word_from_mean_filter_size(self.possible_words)
            # res = palavra
            res = "mixto"
        # elif len(self.chutes) == 3:
        #   res = "jazer"

        else:
            palavra, media = self.select_word_from_mean_filter_size(self.possible_words)
            res = palavra

        self.chutes.append(res)
        return res

    # apply a filter based on guess considering each possible word being the correct one.
    # return the distribution of remaining lenght of possible words after the filter.
    def filter_size_distribution(self, word, possible_words, word_checker: WordChecker):
        results = []
        if len(possible_words) > 200:
            for i in range(243):
                f4 = i % 3
                f3 = i % 9 // 3
                f2 = i % 27 // 9
                f1 = i % 81 // 27
                f0 = i // 81

                feedback = [f0, f1, f2, f3, f4]
                # print(feedback)
                for i, f in enumerate(feedback):
                    if f == 0:
                        feedback[i] = Hint.WRONG_LETTER
                    elif f == 1:
                        feedback[i] = Hint.WRONG_POS
                    elif f == 2:
                        feedback[i] = Hint.RIGHT_POS

                filter = self.word_filter.filter_from_feedback(
                    word,
                    feedback,
                    possible_words,
                )
                # print(word, feedback, filter)
                remaining_words_size = len(filter)
                if remaining_words_size > 0:
                    #                    print(remaining_words_size)
                    results.append(remaining_words_size)
            return results

        for pw in possible_words:
            feedback = word_checker.get_feedback_from_guess(word, pw)
            remaining_words_size = len(
                self.word_filter.filter_from_feedback(
                    word,
                    feedback,
                    possible_words,
                )
            )
            results.append(remaining_words_size)

        return results

    def mean_filter_size(self, word, possible_words, word_checker):
        filter_results = self.filter_size_distribution(
            word, possible_words, word_checker
        )
        mean = sum(filter_results) / len(possible_words)
        return mean

    def max_filter_size(self, word, possible_words, word_checker: WordChecker):
        filter_results = self.filter_size_distribution(
            word, possible_words, word_checker
        )
        max_size = max(filter_results)
        return max_size

    def select_word_from_mean_filter_size(self, possible_words):
        print("LEN POSSIBLE WORDS:", len(possible_words))
        best_max_value = len(possible_words) + 1
        best_mean = best_max_value
        best_word = self.word_list[0]
        word_checker = WordChecker()
        # only one word, sure to win.
        if len(possible_words) == 0:
            raise RuntimeError(
                "select_word_from_mean_filter_size: Empty possible words"
            )

        if len(possible_words) == 1:
            return possible_words[0], 1

        # if there are few remaining possible words, try to use one of them as guess.
        if len(possible_words) < 16:
            for guess in possible_words:
                filter_sizes = self.filter_size_distribution(
                    guess, possible_words, word_checker
                )
                max_value = max(filter_sizes)
                if max_value == 1:
                    # All possible correct words results on remaining words list
                    # with only one word for the current guess.
                    # It is sure to win on next try, at most.
                    return guess, max_value

        #  try to find the guess, among all valid guesses, that minimizes the size of the remaining
        # words. i.e that does the best filtering considering the remaining words.

        for guess in self.word_list:
            filter_sizes = self.filter_size_distribution(
                guess, possible_words, word_checker
            )

            if len(filter_sizes) == 0:
                continue
            mean = sum(filter_sizes) / len(filter_sizes)
            max_value = max(filter_sizes)
            if max_value == 1:
                return guess, max_value
            if max_value <= best_max_value:
                if mean < best_mean or max_value < best_max_value:
                    best_max_value = max_value
                    best_mean = mean
                    best_word = guess
            # print(guess, max_value, mean)
        return best_word, best_max_value


from unidecode import unidecode  #
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
    for i in range(len(palavras_possiveis[0:50])):
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
