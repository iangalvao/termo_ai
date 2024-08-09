from typing import List
from game.controller.icontroller import IController
from game.screen.iscreen_manager import IScreenManager


class IEndMatchController(IController):
    def __init__(self) -> None:
        super().__init__()

    def set_result(self, won: bool, n_attempts: int, words: List[str]):
        pass


class EndMatchScreen(IEndMatchController):
    def __init__(self, screen_manager: IScreenManager) -> None:
        super().__init__()
        self.screen_manager = screen_manager
        screen_manager.bind_controller(self, "end_match_controller")

    def set_result(self, won: bool, n_attempts: int, words: List[str]):
        # print(
        #     f"""END MATCH CONTROLLER SET RESULTS:
        #         \nWON: {won},
        #         \nN_ATTEMPTS: {n_attempts},
        #         \nWORDS: {words},\nPress any key to quit!"""
        # )
        exit(0)

    def process_key(self, key: str) -> None:
        exit(0)
