from typing import Tuple
from game.model.attempt import Attempt
from game.model.hint import *


class Keyboard:
    def __init__(self) -> None:
        self.lines = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        self.state = {}
        for line in self.lines:
            for c in line:
                self.set_letter_hint(c, UNKNOWN_LETTER)

    def process_hints(self, attempt: Attempt):
        for letra, dica, _ in attempt:
            dica_atual = self.get_letter_hint(letra)
            if dica > dica_atual:
                self.set_letter_hint(letra, dica)

    def set_letter_hint(self, letra: str, dica: Hint) -> None:
        self.state[letra] = dica

    def get_letter_hint(self, letra: str) -> Hint:
        return self.state[letra]

    def __iter__(self):
        for i, keyline in enumerate(self.lines):
            res = []
            for c in keyline:
                res.append((c, self.get_letter_hint(c)))
            yield res, i
