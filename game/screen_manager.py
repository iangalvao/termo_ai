###########################################################################
###########################################################################
################                                       ####################
################                SCREEN                 ####################
################                                       ####################
###########################################################################
###########################################################################


from abc import ABC

from game.controller.match_controller import IMatchController
from game.controller.end_game_controller import IEndMatchController
from game.controller.icontroller import IController
from game.iscreen_manager import IScreenManager
from game.model.match import IMatch


class ScreenManager(IScreenManager):
    def __init__(self) -> None:
        super().__init__()
        self.active_controller: IController = None
        self.controllers = {}

    def match_screen(self, n_challenges) -> None:
        match_controller: IMatchController = self.get_controller("match_controller")
        self.set_active_screen(match_controller)
        match_controller.new_match(n_challenges)

    def get_controller(self, controller_id) -> IController:
        return self.controllers[controller_id]

    def end_match_screen(self, match: IMatch) -> None:
        end_match_controller: IEndMatchController = self.get_controller(
            "end_match_controller"
        )
        self.set_active_screen(end_match_controller)
        end_match_controller.set_result(
            match.won(), match.get_n_attempts(), match.get_words()
        )

    def bind_controller(self, controller: IController, controller_id: str) -> None:
        self.controllers[controller_id] = controller

    def set_active_screen(self, controller: IController) -> None:
        self.active_controller = controller

    def process_input(self, key) -> None:
        self.active_controller.process_key(key)
