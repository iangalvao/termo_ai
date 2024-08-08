from unidecode import unidecode
import csv
import sys

from game.controller.controllercore import IInputListener, TerminalInputListener
from game.controller.pygame_input_listener import PygameInputListener

from game.controller.match_controller import MatchController
from game.controller.end_game_controller import EndMatchScreen

from game.screen.screen_manager import IScreenManager, ScreenManager

from game.viewer.game_display import TerminalPresenter
from game.viewer.pygame_presenter import PygameCore
from game.viewer.terminal_manipulator import TerminalCore
from game.viewer.pygame_presenter import pygame_color_dict
from game.viewer.terminal_manipulator import color_dict


# JOGO
class Game:
    def __init__(
        self, input_listener: IInputListener, screen_manager: IScreenManager
    ) -> None:
        self.input_listener: IInputListener = input_listener
        self.screen_manager: IScreenManager = screen_manager

    def run(self) -> None:
        self.screen_manager.match_screen(n_desafios)
        while 1:
            key = self.input_listener.get_input()
            self.screen_manager.process_input(key)


if __name__ == "__main__":

    # ARGS
    if len(sys.argv) > 1:
        try:
            n_desafios = int(sys.argv[1])
        except ValueError:
            print("Please pass a valid integer as argument.")
    else:
        n_desafios = 1

    pygame = False
    if len(sys.argv) > 2:
        display_engine = sys.argv[2]
        if display_engine == "pygame":
            pygame = True

    # DATA
    with open("palavras.csv") as csvfile:
        myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        palavras = next(myreader)
    palavras_unidecode = {}
    for palavra in palavras:
        palavras_unidecode[unidecode(palavra)] = palavra

    # OBJECTS
    if pygame:
        tmanipulator = PygameCore(pygame_color_dict)
        input_listener = PygameInputListener()
    else:
        tmanipulator = TerminalCore(color_dict)
        input_listener = TerminalInputListener()

    grid = [(0, 11 * i) for i in range(n_desafios)]
    if n_desafios > 13:
        grid = [(0, 16 * i) for i in range(8)] + [
            (30, 16 * i) for i in range(n_desafios - 8)
        ]
    presenter = TerminalPresenter(tmanipulator, grid=grid)

    screen_manager = ScreenManager()
    match_controller = MatchController(
        {"pt-br": palavras_unidecode}, presenter, screen_manager
    )
    end_match_controller = EndMatchScreen(screen_manager)

    game = Game(input_listener=input_listener, screen_manager=screen_manager)

    # MAIN LOOP

    game.run()
