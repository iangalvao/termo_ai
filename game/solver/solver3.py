import datetime
import time
from game.model.attempt import Attempt
from game.solver.solver_tools import WordFilter, HintList
from game.model.hint import *
import random
from game.solver.word_checker import WordChecker


class Dummy:
    def __init__(self) -> None:
        pass


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
        self.dict_template = {}
        for i in range(243):
            f4 = str(i % 3)
            f3 = str(i % 9 // 3)
            f2 = str(i % 27 // 9)
            f1 = str(i % 81 // 27)
            f0 = str(i // 81)

            key = f0 + f1 + f2 + f3 + f4
            # dict_template[key] = []
            self.dict_template[key] = 0

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
            res = "ricas"
        elif len(self.chutes) == 1:
            palavra, media, tentativas = self.select_word_from_mean_filter_size(
                self.possible_words
            )
            res = palavra
            # res = "nuvem"

        elif len(self.chutes) == 2:
            palavra, media, tentativas = self.select_word_from_mean_filter_size(
                self.possible_words
            )
            res = palavra
            # res = "jinga"
            # elif len(self.chutes) == 3:
            # res = "ptdob"

        else:
            palavra, media, tries = self.select_word_from_mean_filter_size(
                self.possible_words
            )
            res = palavra

        self.chutes.append(res)
        return res

    # apply a filter based on guess considering each possible word being the correct one.
    # return the distribution of remaining lenght of possible words after the filter.
    def filter_size_distribution(self, guess, possible_words):

        guess_result = self.dict_template.copy()
        for word in possible_words:
            attempt = Attempt(guess, word)
            key = self.feedback_to_key(attempt.feedbacks)
            guess_result[key] += 1

        return [v for k, v in guess_result.items() if v > 0]

    def filter_results(self, guess, possible_words):

        guess_result = self.dict_template.copy()
        for key in guess_result.keys():
            guess_result[key] = []
        for word in possible_words:
            attempt = Attempt(guess, word)
            key = self.feedback_to_key(attempt.feedbacks)
            guess_result[key].append(word)

        return [v for k, v in guess_result.items() if len(v) > 0]

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

    def select_word_from_mean_filter_size(self, possible_words, n_tries=None):
        if len(possible_words) == 0:
            raise RuntimeError(
                "select_word_from_mean_filter_size: Empty possible words"
            )

        if not n_tries:
            n_tries = len(self.chutes)
        # print("LEN POSSIBLE WORDS:", len(possible_words))
        results = {}
        best_max_value = len(possible_words) + 1
        best_mean = best_max_value
        best_word = self.word_list[0]

        # only one word, sure to win.
        if len(possible_words) <= 2:
            # print("TWO OR LESS REMAINING WORDS:",possible_words,n_tries + len(possible_words),)
            return possible_words[0], len(possible_words), n_tries + len(possible_words)

        # if there are few remaining possible words, try to use one of them as guess.
        guesses = self.word_list
        if len(possible_words) < 16:
            guesses = possible_words + self.word_list

        #  try to find the guess, among all valid guesses, that minimizes the size of the remaining
        # words. i.e the one that does the best filtering in the worst case, considering the current remaining words.
        for guess in guesses:
            filter_sizes = self.filter_size_distribution(guess, possible_words)

            if len(filter_sizes) == 0:
                raise RuntimeError("EMPTY FILTER SIZES")
            mean = sum(filter_sizes) / len(filter_sizes)
            max_value = max(filter_sizes)
            if max_value == 1:
                # print("GREAT GUESS:", guess, n_tries + 2)
                return guess, max_value, n_tries + 2
            if max_value <= best_max_value:
                if mean < best_mean or max_value < best_max_value:
                    best_max_value = max_value
                    best_mean = mean
                    best_word = guess
            results[guess] = (max_value, mean)

        consonants = "qrtpsdfgjlzxcvbnm"
        for chute in self.chutes:
            # print("chute:", chute)
            for letter in chute:
                if letter in consonants:
                    consonants = consonants.replace(letter, "")
        # print(feedbacks)

        sorted_list = sorted(results.items(), key=lambda item: (item[1][0], item[1][1]))

        # Convert the list of tuples with word, max, and mean
        sorted_tuples = [word for word, (max_val, mean_val) in sorted_list]
        # print(guess, max_value, mean)

        three_consonants_tuples = []

        for word in sorted_tuples:
            if len([1 for l in set(word) if l in consonants]) >= 3:
                three_consonants_tuples.append(word)

        # Print the sorted list
        # print("BEST WORDS")
        # for word, max_val, mean_val in sorted_tuples[0:100]:
        #   print(f"{word}: max = {max_val}, mean = {mean_val}")

        # print("THREE CONSONANTS BEST WORDS")
        # for word, max_val, mean_val in three_consonants_tuples[0:100]:
        #    print(f"{word}: max = {max_val}, mean = {mean_val}")

        three_regular_consonants_tuples = []

        # print("TWO REGULAR CONSONANTS AND ONE SPECIAL BEST WORDS")

        for word in sorted_tuples:
            if len([1 for l in set(word) if l in consonants]) >= 3:
                if len([1 for l in set(word) if l in "qtpdfghjzxcvb"]) >= 2:
                    three_regular_consonants_tuples.append((word))

        # for word, max_val, mean_val in three_regular_consonants_tuples[0:100]:
        #   print(f"{word}: max = {max_val}, mean = {mean_val}")

        four_regular_consonants_tuples = []

        # print("TWO REGULAR CONSONANTS AND ONE SPECIAL BEST WORDS")

        for word in sorted_tuples:
            if len([1 for l in set(word) if l in consonants]) >= 4:
                four_regular_consonants_tuples.append((word))

        sorted_list_best_guesses = four_regular_consonants_tuples[0:1]
        # print("SORTED LIST FOUR:", sorted_list_best_guesses)

        sorted_list_best_guesses = (
            three_regular_consonants_tuples[0 : 2 - len(sorted_list_best_guesses)]
            + sorted_list_best_guesses
        )
        #   print("SORTED LIST THREE R:", sorted_list_best_guesses)

        n = 0
        three_consonants_tuples_2 = []
        for word in three_consonants_tuples:
            if word not in sorted_list_best_guesses:
                if any(
                    [
                        l
                        for l in set(word)
                        if l
                        not in "".join(
                            w
                            for w in (
                                sorted_list_best_guesses + three_consonants_tuples_2
                            )
                        )
                        and l in consonants
                    ]
                ):
                    three_consonants_tuples_2.append(word)
                    n += 1
                    if n == 2:
                        break
        sorted_list_best_guesses = (
            three_consonants_tuples_2[0 : 4 - len(sorted_list_best_guesses)]
            + sorted_list_best_guesses
        )

        sorted_list_best_guesses = (
            sorted_tuples[0 : 5 - len(sorted_list_best_guesses)]
            + sorted_list_best_guesses
        )
        #  print("SORTED LIST FINAL:", sorted_list_best_guesses)

        n_tries += 1
        best_total_tries = 1000
        for guess in sorted_list_best_guesses:
            # print("TRYING BEST GUESS:", guess, "max:", guess_max, "mean:", guess_mean)
            guess_worst_case_tries = 0
            for word_list in self.filter_results(guess, possible_words):
                if len(word_list) >= len(possible_words):
                    break
                # guess_possible_words = self.word_filter.filter_from_feedback()
                _, max_value, new_n_tries = self.select_word_from_mean_filter_size(
                    word_list, n_tries
                )

                if new_n_tries > guess_worst_case_tries:
                    guess_worst_case_tries = new_n_tries

            if guess_worst_case_tries < best_total_tries:
                best_total_tries = guess_worst_case_tries
                best_word = guess

            # print("GUESS RESULT:", guess, "worst case:", guess_worst_case_tries)

        ##print("BEST WORD/ MAX VALUE :", best_word, best_total_tries)

        return best_word, results[best_word][0], best_total_tries


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
