from unidecode import unidecode
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
        feedbacks = [WRONG_LETTER for l in guess]
        for pos, letter in enumerate(guess):
            # giving position feedback
            if letter == correct_word[pos]:
                feedbacks[pos] = RIGHT_POS
            elif letter in correct_word:
                feedbacks[pos] = WRONG_POS

        # Unmark excess wrong_pos. There should be no more marks for a given
        # letter than the total of this letter in the coorect word. 
        # This includes right_pos marks and wrong_pos ones.
        
        for letter in set(guess):
            letter_indexes = [t[0] for t in enumerate(guess) if t[1] == letter]
            right_pos_hints = len([i for i in letter_indexes if feedbacks[i] == RIGHT_POS])
            max_wrong_pos_hints = correct_word.count(letter) - right_pos_hints
            seen = 0
            for pos in letter_indexes:
                feedback = feedbacks[pos]
                if feedback == WRONG_POS:
                    seen+=1
                    if seen > max_wrong_pos_hints:
                        feedbacks[pos] = WRONG_LETTER
                
        
        return feedbacks








