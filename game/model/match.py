###########################################################################
################                                       ####################
################                 MATCH                 ####################
################                                       ####################
###########################################################################


from typing import List
import unidecode
from game.game_states.end_match_menu import MatchResult
from game.model.challenge import IChallenge
from game.model.imatch import IMatch



class Match(IMatch):
    
    def __init__(self, challenges: List[IChallenge], accepted_words: List[str]) -> None:

        self.challenges: List[IChallenge] = challenges
        self.accepted_words = accepted_words

        self.lim_guesses: int = 5 + len(challenges)
        self.n_attempts: int = 0
        self._won: bool = False

    def won_the_game(self):
        for challenge in self.challenges:
            if not challenge.solved:
                return 0
        return 1

    def get_words(self) -> List[str]:
        return [challenge.get_word() for challenge in self.challenges]

    def get_n_attempts(self) -> int:
        return self.n_attempts

    def get_challenges(self) -> List[IChallenge]:
        return self.challenges



    def check_valid_word(self, word: str) -> bool:
        return word.lower() in self.accepted_words


    def won(self) -> bool:
        return self._won

    def get_results(self):

        return MatchResult(self.won(), self.get_n_attempts(), self.get_words())

    def update(self, guess: str):

        # GANHOU

        # CORRIGE
        for i in range(len(self.challenges)):
            if not self.challenges[i].is_solved():
                self.challenges[i].update(unidecode.unidecode(guess))

        self.n_attempts += 1
        if self.won_the_game():
            self._won = True
            return 1
        # PERDEU
        if self.n_attempts == self.lim_guesses:
            return 1
        return 0
