from abc import ABC
import curses
import random
from re import Match
from time import sleep
from typing import List

from game.model.challenge import Challenge
from game.model.match import IMatch
from game.viewer.terminal_presenter import IGameDisplay


class IMatchController(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.match: IMatch = None

    def proccess_key(self, key: str) -> None:
        pass


class MatchController(IMatchController):
    def __init__(self, accepted_words, presenter: IGameDisplay) -> None:
        super().__init__()
        self.match: IMatch = None
        self.presenter: IGameDisplay = presenter
        self.accepted_words = accepted_words

    def proccess_key(self, key):
        pass

    def add_letter(self, key: str):
        if not key.isalpha():
            return
        res = self.match.input_letter(key)
        if res:
            self.presenter.display_game_screen(self.match.get_challenges)

    def submit_guess(self):
        guess = self.match.submit_guess()
        if not guess:
            return
        if not self.check_valid_word(guess, self.accepted_words):
            self.presenter.print_word_not_accepted(guess)
            return

        end_match = self.match.update(guess)
        self.presenter.display_game_screen(self.match.get_challenges)
        if end_match:
            self.end_match()

    def sort_words(self, n: int) -> List[str]:
        sorted_words = []
        for i in range(n):
            word = ""
            while word not in sorted_words:
                random_number = random.randint(1, len(self.accepted_words) - 1 - 9147)
                palavra = self.accepted_words[9147 + random_number].upper()
                if palavra not in sorted_words:
                    sorted_words.append(palavra)

        return sorted_words

    def new_match(self, n_challenges):

        challenges = []
        # n_challenges = 2

        palavras = self.sort_words(list(self.accepted_words.keys()), n_challenges)
        for i in range(n_challenges):
            challenges.append(Challenge(palavras[i]))
        sorted_words = self.sort_words(self, n_challenges)
        self.match = Match(challenges, sorted_words)
        self.presenter.first_print()
        self.presenter.display_game_screen(challenges)

    def end_match(self):
        if self.match.won():
            self.presenter.print_won_the_game(self.match.tentativas)
        else:
            self.presenter.print_loss_the_game(self.challenges)
        return self.screen_manager.end_match_screen(self.match)
