from unidecode import unidecode
from enum import Enum
from typeguard import typechecked
from abc import ABC
from game.common import *


class IWordChecker(ABC):
    def get_feedback_from_guess(self, guess, correct_word):
        pass


class WordChecker(IWordChecker):
    def __init__(self) -> None:
        self.chutes = []
        self.solved = 0

    def get_feedback_from_guess(self, guess, correct_word):
        correct_letters_count = {l: 0 for l in set(guess)}
        letters_count = {l: 0 for l in set(guess)}

        # Mark all according to rightPos, incorrectPos and wrong
        feedbacks = [WRONG_LETTER for l in guess]
        for pos in range(len(correct_word)):
            letter = guess[pos]
            # giving position feedback
            if letter == correct_word[pos]:
                feedbacks[pos] = RIGHT_POS
                correct_letters_count[letter] += 1
            elif letter in correct_word:
                feedbacks[pos] = WRONG_POS

        # Unmark excess incorrect pos. There should be no more marks for a given
        # letter than the total of this letter in this word. This includes correct
        # position marks and incorrect ones.
        for i in range(len(feedbacks)):
            letter = guess[i]
            feedback = feedbacks[i]
            if feedback == WRONG_POS:
                letters_count[letter] += 1
                occur_in_correct_pos = correct_letters_count[letter]
                total_occur = self.count_letters(correct_word, letter)
                occurence_until_now = letters_count[letter]
                if occur_in_correct_pos + occurence_until_now > total_occur:
                    feedbacks[i] = WRONG_LETTER
        return feedbacks

    def count_letters(self, chute, letra):
        res = 0
        for c in unidecode(chute):
            if unidecode(c) == unidecode(letra):
                res += 1
        return res

    def count_letters_in_wrong_pos_L(self, chute, letra, palavra):
        c = self.count_letters_L(palavra, letra)
        w = self.letters_in_right_pos_L(palavra, chute, letra)
        return c - w

    def count_letters_L(self, chute, letra):
        res = 0
        for c in unidecode(chute):
            if unidecode(c) == unidecode(letra):
                res += 1
        return res

    def letters_in_right_pos_L(self, palavra1, palavra2, letra):
        c_count = 0
        letra = unidecode(letra)
        for i in range(len(palavra2)):
            c1 = unidecode(palavra1[i])
            c2 = unidecode(palavra2[i])
            if c1 == letra:
                if c2 == letra:
                    c_count += 1
        return c_count

    def check_word_L(self, chute, palavra):
        word = []

        for i in range(5):
            dica = WRONG_LETTER
            if unidecode(chute[i]) == unidecode(palavra[i]):
                dica = RIGHT_POS
            elif unidecode(chute[i]) in unidecode(palavra):
                if self.count_letters_in_wrong_pos_L(
                    chute, chute[i], palavra
                ) + self.letters_in_right_pos_L(
                    palavra[: i + 1], chute[: i + 1], chute[i]
                ) >= self.count_letters_L(
                    chute[: i + 1], chute[i]
                ):
                    dica = WRONG_POS
            word.append(dica)

        return word

    ###########################################################################
    ################                                       ####################
    ################                LÓGICA                 ####################
    ################                                       ####################
    ###########################################################################

    ###########################################################################
    ################            CHECAGEM DE LETRAS         ####################
    ###########################################################################
