from abc import ABC, abstractmethod
import random
from typing import Dict, List
from game.controller.controllercore import DELETE, ESC, LEFTARROW, RIGHTARROW
from game.game_states.igame_context import IGameContext
from game.game_states.igame_state import IGameState
from game.model.challenge import Challenge
from game.model.match import Match
from game.viewer.game_display import IGameDisplay


class IMatchController(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def submit_guess(self, guess: str) -> None:
        pass

    def new_match(self, n_challenges: int) -> None:
        pass


class PlayState(IGameState):
    def __init__(
        self, presenter: IGameDisplay, match_controller: IMatchController
    ) -> None:
        super().__init__()
        self.presenter = presenter
        self.match_controler: IMatchController = match_controller

    def on_enter(self, context, n_challenges=None) -> None:
        if n_challenges:
            self.presenter.grid = [(2, 11 * i) for i in range(n_challenges)]
            self.match_controler.new_match(n_challenges)

        self.presenter.first_print()
        self.match_controler.display_game()

    def on_exit(self, context) -> None:
        pass

    def handle_input(self, context: IGameContext, input: str) -> None:
        if not self.match_controler.match.won():
            if input == LEFTARROW:
                self.match_controler.move_cursor_left()
            if input == RIGHTARROW:
                self.match_controler.move_cursor_right()
            if ord("A") <= ord(input) <= ord("Z"):
                self.match_controler.input_letter(input)
            if ord(input) in [10, 13]:
                self.match_controler.submit_guess(context)
                return
            if input == DELETE:
                self.match_controler.delete_letter(self.match_controler.cursor)
            if ord(input) == 127:
                self.match_controler.delete_letter(self.match_controler.cursor - 1)
        else:
            if ord(input) == 27:
                context.change_state(
                    "end_match_state", match=self.match_controler.match
                )
                return
        self.match_controler.display_game()


class MatchController(IMatchController):
    def __init__(
        self,
        presenter: IGameDisplay,
        accepted_words: Dict[str, str] = {"pt-br": ["termo", "terno", "perto"]},
    ) -> None:
        self.input_buffer: str = [" " for i in range(5)]
        self.presenter = presenter
        self.accepted_words = accepted_words
        self.cursor = 0

    def new_match(self, n_challenges, language: str = "pt-br"):
        challenges = []
        selected_words = self.sort_words(
            list(self.accepted_words[language].keys()), n_challenges
        )
        for word in selected_words:
            challenges.append(Challenge(word))
        self.match = Match(challenges, self.accepted_words[language])

    def move_cursor_right(self) -> None:
        if self.cursor < 5:
            self.cursor += 1

    def delete_letter(self, pos: int) -> None:
        if 0 <= pos <= 4:
            self.input_buffer[pos] = " "
        if pos != self.cursor:
            self.move_cursor_left()

    def move_cursor_left(self) -> None:
        if self.cursor > 0:
            self.cursor -= 1

    def input_letter(self, letter) -> str:
        if self.cursor < 5:
            self.input_buffer[self.cursor] = letter
            self.move_cursor_right()
            return letter
        return ""

    def submit_guess(self, context):
        guess = self.get_input_buffer()
        if not guess:
            return
        if not self.match.check_valid_word(guess):
            self.presenter.print_word_not_accepted(guess)
            self.display_game()
            return

        self.presenter.display_buffer(
            "".join(self.input_buffer),
            self.match.get_n_attempts(),
            self.match.get_challenges(),
            self.cursor,
        )

        end_match = self.match.update(guess)
        self.display_game()

        if end_match:
            context.change_state(state_id="end_match_state", match=self.match)

    def get_input_buffer(self):
        if any([x == " " for x in self.input_buffer]):
            return ""
        guess = "".join(self.input_buffer)
        self.input_buffer = [" " for i in range(5)]
        self.cursor = 0
        return guess

    def new_match(self, n_challenges: int, language: str = "pt-br"):

        challenges = []
        selected_words = self.sort_words(
            list(self.accepted_words[language]), n_challenges
        )
        for word in selected_words:
            challenges.append(Challenge(word))
        self.match = Match(challenges, self.accepted_words[language])
        self.presenter.lim_guesses = 5 + n_challenges

    def sort_words(self, word_list: str, n: int) -> List[str]:
        sorted_words = []
        for i in range(n):
            word = ""
            while word not in sorted_words:
                random_number = random.randint(0, len(word_list) - 1)
                if len(word_list) > 10000:
                    random_number = random.randint(9147, len(word_list) - 1)

                word = word_list[random_number].upper()
                if word not in sorted_words:
                    sorted_words.append(word)
                else:
                    word = ""
        return sorted_words

    def display_game(self):

        self.presenter.display_game_screen(self.match)
        self.presenter.display_buffer(
            "".join(self.input_buffer),
            self.match.get_n_attempts(),
            self.match.get_challenges(),
            self.cursor,
        )
