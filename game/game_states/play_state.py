import string
from game.game_engine.controllercore import DELETE, LEFTARROW, RIGHTARROW
from game.controller.match_controller import IMatchController
from game.game_engine.igame_context import IGameContext
from game.game_engine.game_states.igame_state import IGameState
from game.game_engine.buffer import Buffer
from game.viewer.game_display import IGameDisplay



class PlayState(IGameState):
    def __init__(
        self, presenter: IGameDisplay, match_controller: IMatchController
    ) -> None:
        super().__init__()
        self.presenter = presenter
        self.match_controler: IMatchController = match_controller
        self.buffer:Buffer = Buffer(5, string.ascii_uppercase, " ")
        
    def on_enter(self, context, n_challenges=None) -> None:
        if n_challenges:
            self.presenter.start(n_challenges)
            self.match_controler.new_match(n_challenges)
        self.presenter.first_print()
        
        match = self.match_controler.get_match()
        if match:
            self.presenter.display_game_screen(match, self.buffer)
        

    def on_exit(self, context) -> None:
        pass

    def handle_input(self, context: IGameContext, input: str) -> None:
        if not self.match_controler.won():
            if input == LEFTARROW:
                self.buffer.move_cursor_left()

            if input == RIGHTARROW:
                self.buffer.move_cursor_right()

            if ord("A") <= ord(input) <= ord("Z"):  # CHAR
                self.buffer.add_char(input)

            if ord(input) in [10, 13]:  # ENTER
                guess = self.buffer.get_current_guess()
                if guess:
                    self.match_controler.submit_guess(guess)
                    match_results = (
                        self.match_controler.get_results()
                    )  # TODO not on the match controller interface.
                    if match_results:
                        context.change_state(
                            state_id="end_match_state", match=self.match_controler.get_match()
                        )
                        return
                self.buffer.reset()
                return

            if input == DELETE:
                self.buffer.move_cursor_right()
                self.buffer.remove_char()
            if ord(input) == 127:  # BACKSPACCE
                self.buffer.remove_char()
        else:
            if ord(input) == 27:  # ESC
                context.change_state(
                    "end_match_state", match=self.match_controler.get_match()
                )
                return
        match = self.match_controler.get_match()
        if match:
            self.presenter.display_game_screen(
                match, self.buffer
            )  # TODO Change display_game_screen to receive a match object and the input buffer instead of challenge list.

    def display_buffer(self):
        self.presenter.display_buffer(
            "".join(self.input_buffer),
            self.match_controler.get_match().get_n_attempts(),  # TODO change display buffer to use the grid initialized in the on_enter func instead of challenge list
            self.cursor,
        )
