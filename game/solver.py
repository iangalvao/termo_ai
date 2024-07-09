import datetime
import time
from game.solver_tools import WordFilter, HintList
from game.common import *
import random
from game.word_checker import WordChecker


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
        if len(self.possible_words) == 0:
            raise RuntimeError("Empty possible words on Solver.")
        
        self.feedbacks = feedbacks
        self.possible_words = self.word_filter.filter_from_feedback_list(
            self.chutes, feedbacks, self.possible_words
            
        )
        if len(self.chutes) == 0:
            res = "ricas"
        elif len(self.chutes) == 1:
            res = "nuvem"
        elif len(self.chutes) == 2:
            res = "ptdob"
        elif len(self.chutes) == 3:
            palavra, media = self.select_word_from_mean_filter_size(self.possible_words)
            res = palavra
        elif len(self.chutes) == 4:
            palavra, media = self.select_word_from_mean_filter_size(self.possible_words)
            res = palavra
        else:
            palavra, media = self.select_word_from_mean_filter_size(self.possible_words)
            res = palavra
                
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

    def filter_size_distribution(self,word, possible_words, word_checker:WordChecker):
        results = []
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
        filter_results =self.filter_size_distribution(word,possible_words,word_checker) 
        mean = sum(filter_results)/len(possible_words)
        return mean

    def max_filter_size(self, word, possible_words, word_checker:WordChecker):
        filter_results =self.filter_size_distribution(word,possible_words,word_checker) 
        max_size = max(filter_results)
        return max_size

    def select_word_from_mean_filter_size(self, possible_words):
        best_mean = 1000000
        best_word = self.word_list[0]
        word_checker = WordChecker()
        # só uma palavra certa
        if len(possible_words) == 1:
            return possible_words[0], 1
        if len(possible_words) < 16:
            for word in possible_words:
                mean = self.max_filter_size(
                    word, possible_words,  word_checker
                )
                if mean == 1:
                    return word, mean
                
        for word in self.word_list:
            mean = self.max_filter_size(
                word, possible_words,  word_checker
            )
            if mean == 1:
                return word, mean
            if mean < best_mean:
                best_mean = mean
                best_word = word
        return best_word, best_mean


    def filter_test_words(self, test_words, possible_guesses):
        res = set()
        for pg in list(possible_guesses):
            for letter in set(pg):
                filter = {w for w in test_words if letter in w}
                res = res.union(filter)
        return res

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
