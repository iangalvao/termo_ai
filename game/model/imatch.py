from abc import ABC, abstractmethod
from typing import List
from game.game_states.end_match_menu import MatchResult
from game.model.challenge import IChallenge


class IMatch(ABC):
    def __init__(self, challenges: List[IChallenge], accepted_words: List[str]) -> None:
        super().__init__()

    @abstractmethod
    def get_results(self) -> MatchResult:
        pass
    @abstractmethod
    def won(self) -> bool:
        pass
    @abstractmethod
    def get_n_attempts(self) -> int:
        pass
    @abstractmethod
    def get_challenges(self) -> List[IChallenge]:
        pass
    @abstractmethod
    def get_words(self) -> List[str]:
        pass
    @abstractmethod
    def check_valid_word(self, word: str) -> bool:
        pass
    @abstractmethod
    def update(self, guess: str) -> None:
        pass
