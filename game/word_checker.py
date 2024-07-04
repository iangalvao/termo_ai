from unidecode import unidecode
from enum import Enum
from typeguard import typechecked
from abc import ABC


class Hint(Enum):
    NUMBER_OF_LETTERS = 3
    RIGHT_POS = 2
    WRONG_POS = 1
    WRONG_LETTER = 0


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


from abc import ABC


class IHintList(ABC):
    def add(self, c, h, v):
        pass

    def merge(self, other):
        pass

    def __iter__(self):
        pass


class HintList:
    def __init__(self) -> None:
        self.hints = {}

    @typechecked
    def add(self, c: str, hint: Hint, val: int):
        if c not in self.hints.keys():
            self.hints[c] = {}
        if hint not in self.hints[c].keys():
            self.hints[c][hint] = set()

        self.hints[c][hint].add(val)

    def merge(self, other):
        for c, hint, val in other:
            self.add(c, hint, val)

    @typechecked
    def set_char_occurrences(self, c: str, n: int):
        if self.check_hint(c, Hint.NUMBER_OF_LETTERS):
            if n <= list(self.hints[c][Hint.NUMBER_OF_LETTERS])[0]:
                return
        self.hints[c][Hint.NUMBER_OF_LETTERS] = {n}

    def get_char_occurrences(self, c: str):
        if self.check_hint(c, Hint.NUMBER_OF_LETTERS):
            return self.hints[c][Hint.NUMBER_OF_LETTERS]
        return 0

    @typechecked
    def check_hint(self, c: str, hint: Hint):
        if c in self.hints:
            if hint in self.hints[c]:
                return True
        return False

    def __iter__(self):
        for c, char_hint_dict in self.hints.items():
            for hint, value_set in char_hint_dict.items():
                for val in value_set:
                    yield (c, hint, val)


class WordFilter:
    def get_hints_from_guess(self, guess, correct_word):
        hints = HintList()
        for pos in range(len(correct_word)):
            letter = guess[pos]
            # number of occurrences feedback of a letter is limited to the number of occurrences in the guess
            number_of_occurrences_feedback = min(
                self.count_letters(correct_word, letter),
                self.count_letters(guess, letter),
            )
            hints.set_char_occurrences(letter, number_of_occurrences_feedback)

            # giving position feedback
            if letter == correct_word[pos]:
                hints.add(letter, Hint.RIGHT_POS, pos)
            elif letter in correct_word:
                hints.add(letter, Hint.WRONG_POS, pos)
            else:
                hints.add(letter, Hint.WRONG_LETTER, 0)

        return hints

    def get_hints_from_guess_list(self, chutes, palavra_correta):
        all_hints = HintList()
        for chute in chutes:
            all_hints.merge(self.get_hints_from_guess(chute, palavra_correta))
        return all_hints

    @typechecked
    def filter_from_hint_list(self, hint_list: IHintList, possible_words: list[str]):
        filtered_words = possible_words.copy()

        for letter, hint, val in hint_list:
            filtered_words = self.filter_from_hint(hint, letter, val, filtered_words)
        return filtered_words

    @typechecked
    def filter_from_hint(
        self, hint: Hint, letter: str, val: int, original_words: list[str]
    ):
        if hint == Hint.RIGHT_POS:
            filtered_words = [w for w in original_words if w[val] == letter]
        elif hint == Hint.WRONG_POS:
            filtered_words = [
                w for w in original_words if (letter in w and w[val] != letter)
            ]
        elif hint == Hint.WRONG_LETTER:
            filtered_words = [w for w in original_words if letter not in w]

        else:  # Hint.NUMBER OF LETTERS
            filtered_words = [
                w
                for w in original_words
                if len([l for l in w if l == letter.lower()]) >= val
            ]

        return filtered_words

    def count_letters(self, chute, letra):
        res = 0
        for c in unidecode(chute):
            if unidecode(c) == unidecode(letra):
                res += 1
        return res


class Solver:
    def __init__(self, word_checker):
        self.word_checker = word_checker

    def mean_filter_size(self, word, possible_words):
        summation = 0
        for pw in possible_words:
            feedback = [self.word_checker.get_feedback_from_guess(word, pw)]
            remaining_words_size = len(
                self.word_filter.filter_from_hints(
                    feedback,
                    word,
                    possible_words,
                )
            )
            summation += remaining_words_size

        mean = summation / len(possible_words)

        return mean

    def select_word_from_mean_filter_size(self, possible_words):
        best_mean = 1000000
        best_word = self.word_list[0]
        # só uma palavra certa
        if len(possible_words) == 1:
            return possible_words[0], 1
        if len(possible_words) < 12:
            for word in possible_words:
                mean = self.mean_filter_size(word, possible_words)
                if mean == 1:
                    return word, mean

        for word in self.word_list:
            mean = self.mean_filter_size(word, possible_words)
            if mean == 1:
                return word, mean
            if mean < best_mean:
                best_mean = mean
                best_word = word
        return best_word, best_mean


class IGuessList(ABC):
    def add(self, guess, hints):
        pass

    def __iter__(self):
        pass


class GuessList:
    def __init__(self, size) -> None:
        self.size = size
        self.guesses = []

    def add(self, guess: str, hints: IHintList):
        displayable_hints = [0 for c in str]
        for letter in set(guess):
            occur = 0
            hints = hints.hints[letter]
            for val in hints[Hint.RIGHT_POS]:
                displayable_hints[val] = Hint.RIGHT_POS
                occur += 1
            for val in list(hints[Hint.WRONG_POS]).sort():
                occur += 1
                if occur > hints[Hint.NUMBER_OF_LETTERS]:
                    displayable_hints[val] = Hint.WRONG_LETTER
        self.guesses.append((guess, displayable_hints))

    def __iter__(self):
        for guess, hints in self.guesses:
            yield (guess, hints)


class GuessDisplay:
    def __init__(self, guessList: IGuessList) -> None:
        self.guesslist = guessList

    def update(self, guess: str, hint_list: IHintList):
        self.guesslist.add(guess, hint_list)

    def render(self):
        for guess, hints in self.guesslist:
            colored_guess = self.color_guess(guess, hints)
            yield colored_guess
