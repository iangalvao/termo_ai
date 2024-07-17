from abc import ABC
import unidecode
from typeguard import typechecked
from game.hint import *


class IHintList(ABC):
    def add(self, c, h, v):
        pass

    def merge(self, other):
        pass

    def __iter__(self):
        pass


class HintList(IHintList):
    def __init__(self) -> None:
        self.hints = {}

    def add(self, c: str, hint: int, val: int):
        if c not in self.hints.keys():
            self.hints[c] = {}
        if hint not in self.hints[c].keys():
            self.hints[c][hint] = set()

        self.hints[c][hint].add(val)

    def merge(self, other):
        for c, hint, val in other:
            self.add(c, hint, val)

    def set_char_occurrences(self, c: str, n: int):
        if self.check_hint(c, MAX_LETTERS):
            return
        if self.check_hint(c, NUMBER_OF_LETTERS):
            if n <= list(self.hints[c][NUMBER_OF_LETTERS])[0]:
                return

        self.hints[c][NUMBER_OF_LETTERS] = {n}

    def set_max_occurrences(self, c: str, n: int):
        self.hints[c][MAX_LETTERS] = {n}
        if self.check_hint(c, NUMBER_OF_LETTERS):
            del self.hints[c][NUMBER_OF_LETTERS]

    def get_char_occurrences(self, c: str):
        if self.check_hint(c, NUMBER_OF_LETTERS):
            return self.hints[c][NUMBER_OF_LETTERS]
        return 0

    def check_hint(self, c: str, hint: int):
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
    def filter_from_hint_list(self, hint_list: IHintList, possible_words: list[str]):
        filtered_words = possible_words
        for letter, hint, val in hint_list:
            filtered_words = self.filter_from_hint(hint, letter, val, filtered_words)
        return filtered_words

    # no feedbacks. thats from other part of the system
    def filter_from_feedback_list(
        self, chutes: list[str], feedbacks: list[int], possible_words: list[str]
    ):
        hint_list = self.get_hints_from_feedback_list(chutes, feedbacks)

        return self.filter_from_hint_list(hint_list, possible_words)

    # no feedbacks. thats from other part of the system
    def filter_from_feedback(
        self, chute: str, feedback: list[int], possible_words: list[str]
    ):
        hint_list = self.get_hints_from_feedback(chute, feedback)
        return self.filter_from_hint_list(hint_list, possible_words)

    def filter_from_hint(
        self, hint: int, letter: str, val: int, original_words: list[str]
    ):
        match hint:
            case Hint.RIGHT_POS:
                filtered_words = [w for w in original_words if w[val] == letter]
            case Hint.WRONG_POS:
                filtered_words = [
                    w for w in original_words if (letter in w and w[val] != letter)
                ]
            case Hint.WRONG_LETTER:
                filtered_words = [w for w in original_words if letter not in w]
            case Hint.NUMBER_OF_LETTERS:
                filtered_words = [
                    w
                    for w in original_words
                    if len([l for l in w if l == letter]) >= val
                ]
            case Hint.MAX_LETTERS:
                filtered_words = [
                    w
                    for w in original_words
                    if len([l for l in w if l == letter]) == val
                ]

        return filtered_words

    # no more methods. change the rest to hint class
    def get_hints_from_feedback(self, chute, feedback):
        hints = HintList()
        pos = 0
        number_of_letters = {
            c: len(
                [
                    True
                    for i in range(5)
                    if c == chute[i] and feedback[i] != WRONG_LETTER
                ]
            )
            for c in set(chute)
        }
        for pos, (c, d) in enumerate(zip(chute, feedback)):
            if d == RIGHT_POS:
                hints.add(c, d, pos)
            elif d == WRONG_POS:
                hints.add(c, d, pos)
            elif d == WRONG_LETTER:
                max_letters = 0
                for i in range(len(chute)):
                    letra = chute[i]
                    dica = feedback[i]
                    if letra.lower() == c.lower():
                        if dica == WRONG_POS or dica == RIGHT_POS:
                            max_letters += 1
                if max_letters != 0:
                    hints.add(c, WRONG_POS, pos)
                    hints.set_max_occurrences(c, max_letters)
                else:
                    hints.add(c, MAX_LETTERS, 0)
        for c in number_of_letters.keys():
            hints.add(c, NUMBER_OF_LETTERS, number_of_letters[c])
        return hints

    def get_hints_from_feedback_list(self, chutes, feedbacks):
        all_hints = HintList()
        for i in range(len(feedbacks)):
            chute = chutes[i]
            fb = feedbacks[i]
            all_hints.merge(self.get_hints_from_feedback(chute, fb))
        return all_hints


class VocabularyAnalyser:
    def __init__(self, words) -> None:
        self.words = words

    def cluster_letter_by_occurrence(self):
        words = self.words
        threshold = min(len(words) / 40, 1)
        # Calculate the occurrences of each letter in the vocabulary
        letter_occurrences = {}

        result = set()
        while 1:
            for word in words:
                for letter in set(word):
                    if letter in letter_occurrences:
                        letter_occurrences[letter] += 1
                    else:
                        letter_occurrences[letter] = 1

            # index of the letter with max occurrences
            max_letter = max(
                letter_occurrences.keys(), key=lambda x: letter_occurrences.get(x)
            )
            result.add(max_letter)
            words = [w for w in words if max_letter not in w]
            letter_occurrences = {}
            if len(words) < threshold:
                break

        for letter in list(result):
            test = self.words
            for other_letter in result:
                if other_letter != letter:
                    test = [w for w in test if other_letter not in w]
            if len(test) < threshold:
                result.remove(letter)
        return result
