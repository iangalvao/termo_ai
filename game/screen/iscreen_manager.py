from abc import ABC
from game.controller.icontroller import IController
from game.model.imatch import IMatch


class IScreenManager(ABC):
    def __init__(self) -> None:
        super().__init__()

    def match_screen(self, n_Challenges):
        pass

    def menu_screen(self):
        pass

    def ingame_menu(self):
        pass

    def end_match_screen(self, match: IMatch) -> None:
        pass

    def bind_controller(self, controller: IController, controller_id: str) -> None:
        pass

    def get_controller(self, controller_id) -> IController:
        pass

    def process_input(self, key) -> None:
        pass
