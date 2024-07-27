from abc import ABC
import curses
import random
from time import sleep
from typing import Dict, List

from game.model.match import Match
from game.controller.controllercore import DELETE, LEFTARROW, RIGHTARROW
from game.controller.icontroller import IController
from game.model.challenge import Challenge
from game.model.match import IMatch
from game.iscreen_manager import IScreenManager
from game.viewer.terminal_presenter import IGameDisplay


class IMatchController(IController):
    def __init__(self) -> None:
        super().__init__()
        self.match: IMatch = None

    def new_match(self, n_challenges):
        pass


class MatchController(IMatchController):
    def __init__(
        self,
        accepted_words: Dict[str, str],
        presenter: IGameDisplay,
        screen_manager: IScreenManager,
    ) -> None:
        super().__init__()

        self.accepted_words = accepted_words
        self.match: IMatch = None
        self.presenter: IGameDisplay = presenter
        self.accepted_words = accepted_words
        self.screen_manager = screen_manager
        self.screen_manager.bind_controller(self, "match_controller")

    def process_key(self, key):
        if key == LEFTARROW:
            self.match.move_cursor_left()
            self.presenter.display_buffer(
                "".join(self.match.input_buffer),
                self.match.get_n_attempts(),
                self.match.get_challenges(),
                self.match.cursor,
            )
        if key == RIGHTARROW:
            self.match.move_cursor_right()
            self.presenter.display_buffer(
                "".join(self.match.input_buffer),
                self.match.get_n_attempts(),
                self.match.get_challenges(),
                self.match.cursor,
            )
        if ord("A") <= ord(key) <= ord("Z"):
            self.add_letter(key)
        if ord(key) in [10, 13]:
            self.submit_guess()
        if key == DELETE:
            self.match.delete_letter(self.match.cursor)
            self.presenter.display_buffer(
                "".join(self.match.input_buffer),
                self.match.get_n_attempts(),
                self.match.get_challenges(),
                self.match.cursor,
            )

        if ord(key) == 127:
            self.match.delete_letter(self.match.cursor - 1)
            self.presenter.display_buffer(
                "".join(self.match.input_buffer),
                self.match.get_n_attempts(),
                self.match.get_challenges(),
                self.match.cursor,
            )
        # IGNORE OTHER CASES

    def add_letter(self, key: str):
        res = self.match.input_letter(key)
        if res:
            self.presenter.display_game_screen(
                self.match.get_challenges(), self.match.lim_guesses
            )
            self.presenter.display_buffer(
                "".join(self.match.input_buffer),
                self.match.get_n_attempts(),
                self.match.get_challenges(),
                self.match.cursor,
            )

    def submit_guess(self):
        guess = self.match.submit_guess()
        if not guess:
            return
        if not self.match.check_valid_word(guess):
            self.presenter.print_word_not_accepted(guess)
            self.presenter.display_game_screen(
                self.match.get_challenges(), self.match.lim_guesses
            )
            return

        self.presenter.display_buffer(
            "".join(self.match.input_buffer),
            self.match.get_n_attempts(),
            self.match.get_challenges(),
            self.match.cursor,
        )
        end_match = self.match.update(guess)
        self.presenter.display_game_screen(
            self.match.get_challenges(), lim_guesses=self.match.lim_guesses
        )

        if end_match:
            self.end_match()
        else:
            self.presenter.display_buffer(
                "".join(self.match.input_buffer),
                self.match.get_n_attempts(),
                self.match.get_challenges(),
                self.match.cursor,
            )

    def sort_words(self, word_list: str, n: int) -> List[str]:
        sorted_words = []
        for i in range(n):
            word = ""
            while word not in sorted_words:
                random_number = random.randint(9147, len(word_list) - 1)
                word = word_list[random_number].upper()
                if word not in sorted_words:
                    sorted_words.append(word)

        return sorted_words

    def new_match(self, n_challenges: int, language: str = "pt-br"):

        challenges = []
        selected_words = self.sort_words(
            list(self.accepted_words[language].keys()), n_challenges
        )
        for word in selected_words:
            challenges.append(Challenge(word))
        self.match = Match(challenges, self.accepted_words[language])
        self.presenter.lim_guesses = 5 + n_challenges
        self.presenter.first_print()

        self.presenter.display_game_screen(
            challenges, lim_guesses=self.match.lim_guesses
        )
        self.presenter.display_buffer(
            "".join(self.match.input_buffer),
            self.match.get_n_attempts(),
            self.match.get_challenges(),
            self.match.cursor,
        )

    def end_match(self):
        if self.match.won():
            self.presenter.print_won_the_game(self.match.get_n_attempts())
        else:
            self.presenter.print_loss_the_game(self.match.get_challenges())
        return self.screen_manager.end_match_screen(self.match)
