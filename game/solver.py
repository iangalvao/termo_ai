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
        else:
            palavra, media = self.select_word_from_mean_filter_size(self.possible_words)
            res = palavra
                
        self.chutes.append(res)
        return res

    # apply a filter based on guess considering each possible word being the correct one.
    # return the distribution of remaining lenght of possible words after the filter.
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
        best_max_value = len(possible_words)+1
        best_mean = best_max_value
        best_word = self.word_list[0]
        word_checker = WordChecker()
        # only one word, sure to win.
        if len(possible_words) == 0:
            raise RuntimeError ("select_word_from_mean_filter_size: Empty possible words")
        
        
        if len(possible_words) == 1:
            return possible_words[0], 1
        
        # if there are few remaining possible words, try to use one of them as guess.
        if len(possible_words) < 16:
            for word in possible_words:
                filter_sizes = self.filter_size_distribution(
                    word, possible_words,  word_checker
                )
                max_value = max(filter_sizes)
                # it is sure to win on next guess, at most.
                if max_value == 1:
                    return word, max_value
                
        #  try to find the guess, among all valid guesses, that minimizes the size of the remaining
        # words. i.e that does the best filtering considering the remaining words. 
        for word in self.word_list:
            filter_sizes = self.filter_size_distribution(
                word, possible_words,  word_checker
            )
            if len(filter_sizes) == 0:
                continue
            mean = sum(filter_sizes)/len(filter_sizes)
            max_value = max(filter_sizes)
            if mean == 1:
                return word, mean
            if max_value <= best_max_value:
                if mean < best_mean or max_value < best_max_value:
                    best_max_value = max_value
                    best_mean = mean
                    best_word = word
                    
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
