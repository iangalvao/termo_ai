from abc import ABC, abstractmethod
from game.controller.controllercore import DELETE, LEFTARROW, RIGHTARROW
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
        self.match_controler: IMatchController = match_controller

    def on_enter(self, context, n_challenges=None) -> None:
        if n_challenges:
            self.match_controler.new_match(n_challenges)

    def on_exit(self, context) -> None:
        pass

    def handle_input(self, context: IGameContext, input: str) -> None:
        if input == LEFTARROW:
            self.match_controler.move_cursor_left()
        if input == RIGHTARROW:
            self.match_controler.move_cursor_right()
        if ord("A") <= ord(input) <= ord("Z"):
            self.match_controler.input_letter(input)
        if ord(input) in [10, 13]:
            self.match_controler.submit_guess(context)
        if input == DELETE:
            self.match_controler.delete_letter(self.cursor)
        if ord(input) == 127:
            self.match_controler.delete_letter(self.cursor - 1)


class MatchController(IMatchController):
    def __init__(self, presenter: IGameDisplay) -> None:
        self.input_buffer: str = [" " for i in range(5)]
        self.cursor = 0

    def new_match(self, n_challenges):
        pass

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
            self.presenter.display_game_screen(
                self.match.get_challenges(), self.match.lim_guesses
            )
            return

        end_match = self.match.update(guess)
        self.presenter.display_game_screen(
            self.match.get_challenges(), lim_guesses=self.match.lim_guesses
        )

        if end_match:
            context.change_state("end_match_state", match=self.match)

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
