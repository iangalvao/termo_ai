from abc import ABC, abstractmethod
from dataclasses import dataclass
import random
from typing import Dict, List, Optional
from game.model.challenge import Challenge, IChallenge
from game.model.imatch import IMatch
from game.model.match import Match
from game.viewer.game_display import IGameDisplay


@dataclass
class MatchStartParams:
    n_challenges: int
    language: str
    
    
class IMatchController(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def submit_guess(self, guess: str) -> None:
        pass

    @abstractmethod
    def new_match(self, match_params: MatchStartParams) -> None:
        pass

    @abstractmethod
    def won(self)-> bool:
        pass

    @abstractmethod
    def get_results(self):
        pass

    @abstractmethod
    def get_match(self) -> Optional[IMatch]:
        pass


class MatchController(IMatchController):
    def __init__(
        self,
        presenter: IGameDisplay,
        accepted_words: Dict[str, List[str]] = {"pt-br": ["termo", "terno", "perto"]},
    ) -> None:
        self.presenter = presenter
        self.accepted_words = accepted_words
        self.match: Optional[IMatch] = None

    def get_match(self) -> Optional[IMatch]:
        return self.match
    
    def submit_guess(self, guess):
   
        if not guess:
            return
        if not self.match.check_valid_word(guess):
            self.presenter.print_word_not_accepted(guess)
        else:
            self.match.update(guess)

        return

    def new_match(self, match_params:MatchStartParams):
        n_challenges = match_params.n_challenges
        language = match_params.language 
        challenges: List[IChallenge] = []
        selected_words = self.sort_words(
            self.accepted_words[language], n_challenges
        )
        for word in selected_words:
            challenges.append(Challenge(word))
            
        self.match = Match(challenges, self.accepted_words[language])

    def sort_words(self, word_list: List[str], n: int) -> List[str]:
        sorted_words = []
        for i in range(n):
            word = ""
            while word not in sorted_words:
                random_number = random.randint(0, len(word_list) - 1)
                if len(word_list) > 10000:
                    random_number = random.randint(9147, len(word_list) - 1)

                word = word_list[random_number].upper()
                if word not in sorted_words:
                    sorted_words.append(word)
                else:
                    word = ""
        return sorted_words

    def display_game(self):
        self.presenter.display_game_screen(self.match)
