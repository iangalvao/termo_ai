import copy
import csv
import random
import sys
from typing import List

from unidecode import unidecode

from game.model.attempt import Attempt
from game.model.hint import RIGHT_POS, WRONG_LETTER, WRONG_POS, Hint
from game.solver.solver_tools import WordFilter


class Solver:
    def __init__(self, possible_guesses: List[str], possible_words: List[str]) -> None:
        self.possible_guesses: List[str] = possible_guesses
        self.tests: List[str] = possible_words.copy()
        self.original_tests: List[str] = possible_words.copy()
        self.aux_list1 = ["" for _ in range(len(possible_guesses))]
        self.aux_list2 = ["" for _ in range(len(possible_guesses))]
        self.feedbacks = []
        self.word_filter = WordFilter()
        self.chutes = []

    def reset(self):
        self.tests = self.original_tests.copy()
        # print("RESET", self.tests)
        self.chutes = []
        self.feedbacks = []

    def generate_answer(self, feedbacks: List[Hint]):
        if len(self.tests) == 0:
            raise RuntimeError(
                f"Empty possible test words on Solver. No possible solution can be found: {feedbacks}, {self.chutes}."
            )

        self.feedbacks = feedbacks
        if len(self.feedbacks) > 0:
            self.tests = self.word_filter.filter_from_feedback_list(
                self.chutes, feedbacks, self.tests
            )
        if len(self.tests) == 0:
            raise RuntimeError(
                f"Empty possible test words on Solver. No possible solution can be found: {feedbacks}, {self.chutes}."
            )

        if len(self.chutes) == 0:
            generated_guess = "ptdob"
            self.chutes.append(generated_guess)
            return generated_guess

        consonants = "qrtpsdfgjlzxcvbnm"
        for chute in self.chutes:
            # print("chute:", chute)
            for letter in chute:
                if letter in consonants:
                    consonants = consonants.replace(letter, "")
        # print(feedbacks)
        print("Remaining Words len:", len(self.tests))
        sys.stdout.flush()
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
        if len(self.tests) < 3:
            self.chutes.append(self.tests[0])
            return self.tests[0]

        for guess in self.possible_guesses:
            # guess_result = copy.deepcopy(dict_template)
            guess_result = dict_template.copy()
            for word in self.tests:
                attempt = Attempt(guess, word)
                key = self.feedback_to_key(attempt.feedbacks)
                #    guess_result[key].append(word)
                guess_result[key] += 1

            i += 1
            s = 0
            m = 0
            c = 0
            for value in guess_result.values():
                # value = len(value)
                if value > 0:
                    s += value
                    if value > m:
                        m = value
                    c += 1
            # result[guess] = guess_result

            # print(guess, i)
            if c == 0:
                # print(guess, s, m, i)
                pass
            else:
                s = s / c
                # print(f"{guess}: max = {m}, mean = {s}")
                result[guess] = (m, s, c)
            if m == 1:
                # print(f"{guess}: max = {m}, mean = {s}")
                self.chutes.append(guess)
                return guess
        # Sorting the dictionary items based on max value first, then mean value
        sorted_list = sorted(result.items(), key=lambda item: (item[1][0], item[1][1]))

        # Convert the list of tuples with word, max, and mean
        sorted_tuples = [
            (word, max_val, mean_val)
            for word, (max_val, mean_val, count) in sorted_list
        ]
        three_consonants_tuples = []

        for word, max_val, mean_val in sorted_tuples:
            if len([1 for l in set(word) if l in consonants]) >= 3:
                three_consonants_tuples.append((word, max_val, mean_val))

        # Print the sorted list
        # print("BEST WORDS")
        # for word, max_val, mean_val in sorted_tuples[0:100]:
        #   print(f"{word}: max = {max_val}, mean = {mean_val}")

        # print("THREE CONSONANTS BEST WORDS")
        # for word, max_val, mean_val in three_consonants_tuples[0:100]:
        #    print(f"{word}: max = {max_val}, mean = {mean_val}")

        three_regular_consonants_tuples = []

        # print("TWO REGULAR CONSONANTS AND ONE SPECIAL BEST WORDS")

        for word, max_val, mean_val in sorted_tuples:
            if len([1 for l in set(word) if l in consonants]) >= 3:
                if len([1 for l in set(word) if l in "qtpdfghjzxcvb"]) >= 2:
                    three_regular_consonants_tuples.append((word, max_val, mean_val))

        # for word, max_val, mean_val in three_regular_consonants_tuples[0:100]:
        #   print(f"{word}: max = {max_val}, mean = {mean_val}")

        four_regular_consonants_tuples = []

        # print("TWO REGULAR CONSONANTS AND ONE SPECIAL BEST WORDS")

        for word, max_val, mean_val in sorted_tuples:
            if len([1 for l in set(word) if l in consonants]) >= 4:
                four_regular_consonants_tuples.append((word, max_val, mean_val))

        generated_guess = sorted_tuples[0][0]

        if (len(self.chutes) == 1) and (len(four_regular_consonants_tuples) > 0):

            generated_guess = four_regular_consonants_tuples[0][0]

        elif len(self.chutes) <= 3:
            if len(three_regular_consonants_tuples) > 0:

                generated_guess = three_regular_consonants_tuples[0][0]
                # print("GENERATED THREE LETTER CONSONANT GUESS:", generated_guess)
            elif len(three_consonants_tuples) > 0:
                # print("NO NEW THREE LETTER CONSONANT")
                generated_guess = three_consonants_tuples[0][0]

        self.chutes.append(generated_guess)
        return generated_guess

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

    with open("palavras.csv") as csvfile:
        myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        palavras_originais = next(myreader)
    palavras_unidecode = {}
    for palavra in palavras_originais:
        palavras_unidecode[unidecode(palavra)] = palavra
    palavra_possiveis = list(palavras_unidecode.keys())[9147:]

    # lista_unidecode = ["arara", "arame", "morno", "azedo", "amado", "ximbo", "pizza"]
    # palavra_possiveis = ["morno", "azedo", "amado", "ximbo", "pizza"]
    return (
        list(palavras_unidecode.keys()),
        palavra_possiveis,
    )


if __name__ == "__main__":
    palavras_unidecode, palavras_possiveis = init_game()
    word_filter = WordFilter()
    random.shuffle(palavras_unidecode)
    tests = palavras_unidecode
    # tests = palavras_possiveis
    solver = Solver(palavras_unidecode, tests, word_filter)
    for i in range(243):
        solver.chutes = ["licor"]
        f4 = str(i % 3)
        f3 = str(i % 9 // 3)
        f2 = str(i % 27 // 9)
        f1 = str(i % 81 // 27)
        f0 = str(i // 81)

        feedback = [f0, f1, f2, f3, f4]

        for i, f in enumerate(feedback):
            if f == "0":
                feedback[i] = Hint.WRONG_LETTER
            elif f == "1":
                feedback[i] = Hint.WRONG_POS
            elif f == "2":
                feedback[i] = Hint.RIGHT_POS
        print(feedback)
        feedback = [feedback]
    feedback = []
    results = solver.generate_answer(feedback)
    solver.reset()
