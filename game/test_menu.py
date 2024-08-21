import csv
import sys

from unidecode import unidecode
from game.controller.controllercore import IInputListener, TerminalInputListener
from game.controller.end_game_controller import (
    BaseMenuPresenter,
    EndMatchMenuPresenter,
    MatchConfigState,
    QuitPresenter,
    QuitState,
    ScreenManager,
)
from game.game_states.end_match_menu import EndMatchState
from game.game_states.igame_context import IGameContext
from game.game_states.igame_state import IGameState
from game.game_states.main_menu import MainMenu, MainMenuState
from game.game_states.play_state import MatchController, PlayState
from game.viewer.game_display import TerminalPresenter
from game.viewer.terminal_manipulator import TerminalCore, color_dict


class StateFactory:
    def __init__(self, accepted_words):
        screen_manager = ScreenManager(22, 80)
        display_core = TerminalCore(color_dict)
        main_menu_presenter = BaseMenuPresenter(screen_manager, display_core)
        end_game_presenter = EndMatchMenuPresenter(screen_manager, display_core)
        match_presenter = TerminalPresenter(display_core)
        match_controller = MatchController(
            match_presenter, accepted_words=accepted_words
        )
        quit_presenter = QuitPresenter(screen_manager, display_core)
        self.states = {
            "main_menu_state": MainMenuState(main_menu_presenter),
            "play_state": PlayState(match_presenter, match_controller),
            "quit_state": QuitState(quit_presenter),
            "match_config": MatchConfigState(main_menu_presenter),
            "end_match_state": EndMatchState(end_game_presenter),
        }

    def get_state(self, state_id, **kwargs):
        return self.states.get(state_id)


class GameContext(IGameContext):
    def __init__(self, state_factory: StateFactory):
        self.state_factory = state_factory
        self.current_state = self.state_factory.get_state("main_menu_state")
        self.running = True
        self.current_state.on_enter(self)

    def change_state(self, state_id, **kwargs):
        if self.current_state:
            self.current_state.on_exit(self)
        self.current_state = self.state_factory.get_state(state_id)
        if self.current_state:
            self.current_state.on_enter(self, **kwargs)
        else:
            print(f"State '{state_id}' does not exist.")

    def handle_input(self, input):
        if self.current_state:
            self.current_state.handle_input(self, input)
        else:
            print("No current state to handle input.")


def first_print():
    print("-------------O TERMO TERMINAL--------------")
    print("versão para terminal de https://www.term.ooo")
    # Limpa a tela
    s = ""
    for i in range(80):
        s += " "
    for i in range(21):
        print(s)
    print(f"\033[{22}A", end="")
    sys.stdout.flush()


class Game:
    def __init__(self, input_listener: IInputListener, context: IGameContext) -> None:
        self.input_listener: IInputListener = input_listener
        self.context = context

    def run(self) -> None:
        while 1:
            key = self.input_listener.get_input()
            self.context.handle_input(key)


if __name__ == "__main__":

    # DATA
    with open("palavras.csv") as csvfile:
        myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        palavras = next(myreader)
    palavras_unidecode = {}
    for palavra in palavras:
        palavras_unidecode[unidecode(palavra)] = palavra
    lista_unidecode = list(palavras_unidecode.keys())
    first_print()
    state_factory = StateFactory({"pt-br": lista_unidecode})
    input_listener = TerminalInputListener()
    context = GameContext(state_factory)
    game = Game(input_listener, context)
    game.run()
