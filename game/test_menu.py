from game.controller.end_game_controller import MatchConfigState, QuitState
from game.game_states.end_match_menu import EndMatchState
from game.game_states.igame_context import IGameContext
from game.game_states.igame_state import IGameState
from game.game_states.main_menu import MainMenu, MainMenuState
from game.game_states.play_state import PlayState


class StateFactory:
    def __init__(self):
        self.states = {
            "main_menu": MainMenuState(),
            "gameplay": PlayState(),
            "quit": QuitState(),
            "match_config": MatchConfigState(),
            "end_game": EndMatchState(),
            # Static states can be pre-instantiated
        }

    def get_state(self, state_name, **kwargs):
        return self.states.get(state_name)


class GameContext(IGameContext):
    def __init__(self, state_factory: StateFactory):
        self.state_factory = state_factory
        self.current_state = self.state_factory.get_state("main_menu")
        self.running = True
        self.current_state.on_enter(self)

    def change_state(self, state_name, **kwargs):
        if self.current_state:
            self.current_state.on_exit(self)
        self.current_state = self.state_factory.get_state(state_name, **kwargs)
        if self.current_state:
            self.current_state.on_enter(self)
        else:
            print(f"State '{state_name}' does not exist.")

    def handle_input(self, input):
        if self.current_state:
            self.current_state.handle_input(self, input)
        else:
            print("No current state to handle input.")
