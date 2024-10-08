import random
import sys
from typing import List, TextIO
from game.solver.word_checker import WordChecker
from abc import ABC
from game.model.hint import *
from game.solver.solver3 import Solver


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

    def print(self):
        for k, n in self._children.keys():
            print(k)


class Tree:
    def __init__(self, root_word=None) -> None:
        self.root: Node = Node(root_word)
        if root_word:
            self.depth = 0
        else:
            self.depth = 1

    def add(self, feedbacks, guess):
        node = self.root

        depth = 1
        for fb in feedbacks:
            k = self.feedback_to_key(fb)
            if not k:
                return  # This should be a error
            if node.children(k):
                node = node.children(k)
                depth += 1
            else:
                node = self.add_children(node, k, guess)
        if depth > self.depth:
            self.depth = depth

    def get_node(self, feedbacks):
        node = self.root
        for fb in feedbacks:
            k = self.feedback_to_key(fb)
            if not k:
                return None
            if node.children(k):

                node = node.children(k)
            else:
                return None
        return node

    def add_children(self, node, k, guess):
        if node:
            new_node = Node(guess)
            node._children[k] = new_node
        else:
            self.root = Node(guess)

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

    def print(self):
        node = self.root
        children = node._children.keys()
        print(self.root.word)

        for children in children:
            c = node.children(children)
            if c.word:
                print(c.word)

    def print_rec(self):
        self.print_node(self.root, 0)

    def print_node(self, node: Node, depth):
        if not node:
            return
        padding = "    " * depth

        if node.word:
            print(padding + node.word)
        else:
            print("node without word")

        children = set()
        for n in node._children.values():
            children.add(n)
        for i, (n) in enumerate(children):

            self.print_node(n, depth + 1)

    def print_d_node(self, node: Node, depth):
        padding = "   "
        if len(node.keys() == 0):
            if node.word:
                print(padding + node.word)
            else:
                print("node without word")
            return

        children = set()
        for n in node.values():
            children.add(n)
        for i, (k, n) in enumerate(node.items()):
            if k != "word":
                self.print_d_node(n, depth + 1)

    def print_nodes_and_keys(self):
        self.print_node_and_keys_rec(self.root, 0)

    def print_nodes_and_keys_padding(self, padding):
        self.print_node_and_keys_rec(self.root, 0, padding)

    def print_node_and_keys_rec(self, node, depth, padding_arg=None):
        if not node:
            return
        if padding_arg == None:
            padding = "    " * depth
        else:
            padding = padding_arg * depth
        if node.word:
            print(padding + node.word + str(depth))
        else:
            print("node without word")

        children = set()
        for n in node._children.values():
            children.add(n)

        for n in children:
            keys = [key for key, value in node._children.items() if value == n]
            for k in keys:
                print(padding + k + str(depth))
            self.print_node_and_keys_rec(n, depth + 1, padding_arg)

    def get_nodes_by_level(self):
        nodes = [[] for i in range(self.depth)]
        self.get_nodes_by_level_rec(self.root, 0, nodes)
        return nodes

    def get_nodes_by_level_rec(self, node, depth, nodes):
        if not node:
            return
        print(node.word, depth)
        nodes[depth].append(node)
        children = set()
        for n in node._children.values():
            children.add(n)

        for n in children:
            self.get_nodes_by_level_rec(n, depth + 1, nodes)

    def generate_answer(self, feedbacks):
        node = self.get_node(feedbacks)
        return node.word


class TreeBuilder:
    def __init__(self, words) -> None:
        self.word_checker = WordChecker()
        self.words = words

    def make_tree(self, solver: ISolver):

        first_guess = solver.generate_answer([])
        print("first_guess", first_guess)
        tree = Tree(root_word=first_guess)
        solver.reset()
        tentativas = [0 for i in range(10)]
        for w in self.words:
            # print(w)
            feedbacks = []
            guess = first_guess
            print("CORRECT WORD:", w)
            sys.stdout.flush()
            n = 0
            while w != guess:
                node = tree.get_node(feedbacks)
                if node:
                    guess = node.word
                    # print("GUESSES:", solver.chutes, "FEEDBACKS:", feedbacks)
                    print("READY GUESS", guess)
                    sys.stdout.flush()
                    solver.chutes.append(
                        guess
                    )  # Solver didn't generate response, add it to it's guess list.
                else:
                    # print("GUESSES:", solver.chutes, "FEEDBACKS:", feedbacks)
                    guess = solver.generate_answer(feedbacks)
                    print("GENERATED GUESS", guess)
                    sys.stdout.flush()
                # print(" "+guess)
                tree.add(feedbacks, guess)
                fb = wchecker.get_feedback_from_guess(guess, w)
                feedbacks.append(fb)
                n += 1
                # print(guess)
                if guess == w:
                    print(f"Ganhou. Palavra: {w} número de tentativas: {n}")
                    tentativas[n - 1] += 1
                    print(tentativas)
                    sys.stdout.flush()
                    break

            solver.reset()
        return tree

    def read_from_string(self, string: str):
        pass

    # leu string, cria node com string (ou só retorna ele, se não existir) e adiciona no pai com a chave
    # leu numero chama recursivo (parent = node, key)
    def read_from_string_rec(self, parent: Node, key: str, file: TextIO, d: int):
        line = file.readline()
        if line:
            val, depth = line.split()
        else:
            return
        if any([l for l in val if l.isalpha()]):
            node = Node(val)
            parent._children[key] = node
            line = file.readline()
        elif self.is_feedback(val):
            pass
            d = self.read_from_string_rec(node, val, depth)
        if d > depth:
            return d

    pass

    # leu string, cria node com string (ou só retorna ele, se não existir) e adiciona no pai com a chave
    # leu numero chama recursivo (parent = node, key)
    def read_from_string(self, file: TextIO, d: int):
        tree = Tree()
        last_nodes: List[Node] = [None for i in range(50)]
        max_depth = 0
        for line in file:
            if line:
                # print(line.strip())
                val = line[:5]
                if any([l for l in val if l.isalpha()]):
                    depth = int(line[5])
                    if depth > max_depth:
                        max_depth = depth
                    if depth == 0:
                        node = tree.root
                        node.set_word(val)
                    else:
                        node = Node(val)
                        last_nodes[depth - 1]._children[key] = node
                    last_nodes[depth] = node
                else:
                    key = val
        tree.depth = max_depth + 1
        return tree


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

    solver = None

    return (
        n_desafios,
        lim_chutes,
        lista_unidecode,
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
    testes = palavras_possiveis

    # palavras_unidecode = ["arara", "arame", "todos", "virus", "belos"]
    # testes = ["todos", "virus", "belos"]
    random.shuffle(palavras_unidecode)
    testes = palavras_unidecode  # [0:2000]
    testes = palavras_possiveis
    treebuilder = TreeBuilder(testes)
    solver = Solver(palavras_unidecode, possible_words=testes)

    tree = treebuilder.make_tree(solver)
    tree.print_nodes_and_keys_padding("")

    # for i in range(len(palavras_possiveis)):
    #     palavra = unidecode(palavras_possiveis[i])
    #     feedbacks = []
    #     for i in range(6):
    #         guess = solver.generate_answer(feedbacks)
    #         print(guess)
    #         if guess != palavra:
    #             fb = wchecker.get_feedback_from_guess(guess, palavra)
    #             feedbacks.append(fb)
    #         else:
    #             print("Ganhou")
    #             break
    #     solver.reset()
    #     tree.ad
