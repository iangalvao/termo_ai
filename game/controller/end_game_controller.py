from typing import List
from game.controller.icontroller import IController


class IEndMatchController(IController):
    def __init__(self) -> None:
        super().__init__()

    def set_result(self, won: bool, n_attempts: int, words: List[str]):
        pass


class EndMatchController(IEndMatchController):
    def __init__(self) -> None:
        super().__init__()

    def set_result(self, won: bool, n_attempts: int, words: List[str]):
        print(
            f"""END MATCH CONTROLLER SET RESULTS:
                WON: {won}, 
                N_ATTEMPTS: {n_attempts}, 
                WORDS: {words},\nPress any key to quit!"""
        )

    def process_input(self, key: str) -> None:
        exit(0)
