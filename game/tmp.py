from abc import ABC
from typing import Iterator, List, Tuple

from game.model.hint import ComparableEnum
from game.viewer.colored_string import ColoredString


class Hint(ComparableEnum):
    NUMBER_OF_LETTERS = 3
    RIGHT_POS = 2
    WRONG_POS = 1
    WRONG_LETTER = 0
    MAX_LETTERS = 4
    UNKNOWN_LETTER = -1


class IAttempt(ABC):
    def __init__(self, guess: str, correct_word: str) -> None:
        super().__init__()

    def get_feedbacks(self) -> list[Hint]:
        pass

    def get_guess(self) -> str:
        pass

    def __iter__(self) -> Iterator[Tuple[str, str, int]]:
        pass


class IKeyboard(ABC):
    def __init__(self) -> None:
        super().__init__()

    def process_hints(self, attempt: IAttempt) -> None:
        pass

    def get_letter_hint(self, letter: str) -> Hint:
        pass

    def __iter__(self):
        pass


class IChallenge(ABC):
    def __init__(self) -> None:
        super().__init__()

    def get_lim_guesses(self) -> int:
        pass

    def get_attempts(self) -> list[IAttempt]:
        pass

    def get_keyboard(self) -> IKeyboard:
        pass

    def get_word(self) -> str:
        pass

    def update(self) -> IAttempt:
        pass


class IMatch(ABC):
    def __init__(self, challenges: List[IChallenge], accepted_words: List[str]) -> None:
        super().__init__()

    def get_n_attempts(self) -> int:
        pass

    def get_challenges(self) -> List[IChallenge]:
        pass

    def get_words(self) -> List[str]:
        pass

    def move_cursor_left(self) -> None:
        pass

    def move_cursor_right(self) -> None:
        pass

    def input_letter(self) -> str:
        pass

    def won(self) -> bool:
        pass

    def submit_guess(self) -> str:
        pass

    def check_valid_word(self, word: str) -> bool:
        pass

    def update(self, guess: str) -> None:
        pass


class IInputListener(ABC):
    def __init__(self) -> None:
        super().__init__()

    def get_input(self) -> str:
        pass


class IController(ABC):
    def __init__(self) -> None:
        super().__init__()

    def process_input(self, key: str) -> None:
        pass


class IMatchController(IController):
    def __init__(self) -> None:
        super().__init__()
        self.match: IMatch = None

    def new_match(self, n_challenges):
        pass


class IEndMatchController(IController):
    def __init__(self) -> None:
        super().__init__()

    def set_result(self, won: bool, n_attempts: int, words: List[str]):
        pass


class IScreen(ABC):
    def __init__(self) -> None:
        pass

    def add(self, colored_string: ColoredString, pos: Tuple[int, int]):
        pass

    def merge(self, other: object):
        pass

    def __iter__(self):
        pass

    def __eq__(self, value: object) -> bool:
        pass

    def __str__(self) -> str:
        pass


class IDisplayCore(ABC):
    def __init__(self) -> None:
        super().__init__()

    def go_to_pos(self, pos: Tuple[int, int]) -> str:
        pass

    def print_at_pos(self, s: str, pos: Tuple[int, int]) -> None:
        pass

    def print_colored_string(self, colored_string: ColoredString, pos: Tuple[int, int]):
        pass

    def clear_line(self, n: int) -> None:
        pass

    def print_screen(self, screen: IScreen):
        pass


class Message:
    def __init__(self) -> None:
        pass


class IGameDisplay(ABC):
    def __init__(self, tmanipulator: IDisplayCore) -> None:
        super().__init__()

    def display_challenge(self, challenge: IChallenge, pos: Tuple[int]) -> None:
        pass

    def display_intro(self) -> None:
        pass

    def display_message(self, message: Message) -> None:
        pass

    def display_game_screen(self, challenges: List[IChallenge]) -> None:
        pass


class IScreenManager(ABC):
    def __init__(self) -> None:
        super().__init__()

    def match_screen(self, n_challenges):
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
