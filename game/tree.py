from game.word_checker import WordChecker
from abc import ABC
from common import Hint
from solver2 import Solver

class ISolver(ABC):
    def generate_answer(self, feedbacks):
        pass


class Node:
    def __init__(self, word=None) -> None:
        self._children = {}
        self.word = word

    def children(self, k):
        if k in self._children:
            return self._children[k]
        else:
            return None

    def set_word(self, w):
        self.word = w

    def add_children(self, k):
        self._children[k] = Node()

class Tree:
    def __init__(self, root_word=None) -> None:
        self.root = Node(root_word)

    def add(self, feedbacks, guess):
        node = self.root
        for fb in feedbacks:
            k = self.feedback_to_key(fb)
            if node.children(k):
                node = node.children(k)
            else:
                node = node.add_children(k)
        node.set_word(guess)

    def feedback_to_key(self, fb):
        s = ""
        for i in fb:
            if i == Hint.RIGHT_POS:
                s += "2"
            elif i == Hint.WRONG_POS:
                s += "1"
            elif i == Hint.WRONG_LETTER:
                s += "0"
        return s


class TreeBuilder:
    def __init__(self, words) -> None:
        self.word_checker = WordChecker()
        self.words = words

    def make_tree(self, solver: ISolver):
        first_guess = solver.genrate_answer([])
        tree = Tree(root_word=first_guess)
        for w in self.words:
            feedbacks = []
            guess = first_guess
            while w != guess:
                if guess != palavra:
                    fb = wchecker.check_word_L(guess, palavra)
                    feedbacks.append(fb)
                else:
                    print("Ganhou")
                    break
                guess = solver.generate_answer(feedbacks)
                print(guess)
                tree.add(feedbacks, guess)
            solver.reset()

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
        for i in range(6):
            guess = solver.generate_answer(feedbacks)
            print(guess)
            if guess != palavra:
                fb = wchecker.check_word_L(guess, palavra)
                feedbacks.append(fb)
            else:
                print("Ganhou")
                break
        solver.reset()
