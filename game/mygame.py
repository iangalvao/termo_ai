from abc import ABC
from typing import Dict, List, Tuple
from unidecode import unidecode
import csv
import sys
import random
from colorama import Fore, Back, Style
from game.controller.controller import MatchController
from game.controller.controllercore import IInputListener, TerminalInputListener
from game.controller.end_game_controller import EndMatchController
from game.controller.pygame_input_listener import PygameInputListener
from game.model.challenge import Challenge
from game.model.hint import *
from game.model.keyboard import Keyboard
from game.screen_manager import IScreenManager, ScreenManager
from game.viewer.pygame_presenter import PygameCore
from game.viewer.terminal_presenter import (
    IChallenge,
    IGameDisplay,
    Message,
    TerminalPresenter,
)
from game.viewer.pygame_presenter import pygame_color_dict
from game.viewer.terminal_manipulator import color_dict
from game.solver.word_checker import IWordChecker, WordChecker
from game.model.attempt import Attempt
from game.viewer.terminal_manipulator import IDisplayCore, TerminalCore

###########################################################################
###########################################################################
################                                       ####################
################                 MENU                  ####################
################                                       ####################
###########################################################################
###########################################################################


###########################################################################
###########################################################################
################                                       ####################
################                 JOGO                  ####################
################                                       ####################
###########################################################################
###########################################################################


class Game:
    def __init__(
        self, input_listener: IInputListener, screen_manager: IScreenManager
    ) -> None:
        self.input_listener: IInputListener = input_listener
        self.screen_manager = screen_manager

    def run(self) -> None:
        while 1:
            key = self.input_listener.get_input()
            self.screen_manager.proccess_input(key)

            # self.presenter.tmanipulator.clear_line(12)  # Apaga mensagens.
            # self.presenter.display_game_screen(self.challenges)


###########################################################################
################                                       ####################
################                 INIT                  ####################
################                                       ####################
###########################################################################

if __name__ == "__main__":

    ###########################################################################
    ################                ARGS                   ####################
    ###########################################################################
    if len(sys.argv) > 1:
        try:
            # Convert the argument to an integer and store it in a variable
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

    ###########################################################################
    ################                DATA                   ####################
    ###########################################################################
    with open("palavras.csv") as csvfile:
        myreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        palavras = next(myreader)
    palavras_unidecode = {}
    for palavra in palavras:
        palavras_unidecode[unidecode(palavra)] = palavra

    ###########################################################################
    ################              OBJECTS                  ####################
    ###########################################################################
    if pygame:
        tmanipulator = PygameCore(pygame_color_dict)
        input_listener = PygameInputListener()
    else:
        tmanipulator = TerminalCore(color_dict)
        input_listener = TerminalInputListener()

    grid = [(0, 16 * i) for i in range(n_desafios)]
    presenter = TerminalPresenter(tmanipulator, grid=grid)

    match_controller = MatchController(presenter)
    end_match_controller = EndMatchController()
    screenmanager = ScreenManager(match_controller, end_match_controller)

    game = Game(input_listener=input_listener)

    ###########################################################################
    ################             MAIN LOOP                 ####################
    ###########################################################################

    game.run()


#    padding = 4
#    spacing = 16
