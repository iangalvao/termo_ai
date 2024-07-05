from game.word_checker import WordChecker
from solver import Solver
from abc import ABC
from common import Hint


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
                feedback = self.word_checker.get_feedback_from_guess(guess, w)
                feedbacks.append(feedback)
                guess = solver.generate_answer(feedbacks)
                tree.add(feedbacks, guess)
