from unidecode import unidecode
from enum import Enum
from typeguard import typechecked
from abc import ABC
from common import Hint


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
        feedbacks = [Hint.WRONG_LETTER for l in guess]
        for pos in range(len(correct_word)):
            letter = guess[pos]
            # giving position feedback
            if letter == correct_word[pos]:
                feedbacks[pos] = Hint.RIGHT_POS
                correct_letters_count[letter] += 1
            elif letter in correct_word:
                feedbacks[pos] = Hint.WRONG_POS

        # Unmark excess incorrect pos. There should be no more marks for a given
        # letter than the total of this letter in this word. This includes correct
        # position marks and incorrect ones.
        for i in range(len(feedbacks)):
            letter = guess[i]
            feedback = feedbacks[i]
            if feedback == Hint.WRONG_POS:
                letters_count[letter] += 1
                occur_in_correct_pos = correct_letters_count[letter]
                total_occur = self.count_letters(correct_word, letter)
                occurence_until_now = letters_count[letter]
                if occur_in_correct_pos + occurence_until_now > total_occur:
                    feedbacks[i] = Hint.WRONG_LETTER
        return feedbacks

    def count_letters(self, chute, letra):
        res = 0
        for c in unidecode(chute):
            if unidecode(c) == unidecode(letra):
                res += 1
        return res

    ###########################################################################
    ################                                       ####################
    ################                LÓGICA                 ####################
    ################                                       ####################
    ###########################################################################

    ###########################################################################
    ################            CHECAGEM DE LETRAS         ####################
    ###########################################################################
