###########################################################################
###########################################################################
################                                       ####################
################                SCREEN                 ####################
################                                       ####################
###########################################################################
###########################################################################


from abc import ABC

from game.controller.controller import IMatchController
from game.controller.end_game_controller import IEndMatchController
from game.controller.icontroller import IController
from game.model.match import IMatch


class IScreenManager(ABC):
    def __init__(self) -> None:
        super().__init__()

    def new_match(self, match: IMatch):
        pass

    def menu_screen(self):
        pass

    def ingame_menu(self):
        pass

    def end_match_screen(self, match: IMatch):
        pass

    def get_match_controller(self, n_challenges):
        pass


class ScreenManager(IScreenManager):
    def __init__(
        self,
        match_controller: IMatchController,
        end_match_controller: IEndMatchController,
    ) -> None:
        super().__init__()
        self.match_controller: IMatchController = match_controller
        self.end_match_controller: IEndMatchController = end_match_controller
        self.active_controller: IController = self.match_controller

    def end_match_screen(self, match: IMatch):
        self.end_match_controller.set_result(
            match.won, match.n_attempts, match.get_words()
        )
        self.set_active_screen(self.end_match_controller)

    def process_input(self, key):
        self.active_controller.process_key(key)
