from typing import Tuple
from game.common import *
class Keyboard:
    def __init__(self) -> None:
        self.lines = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        self.state = {}
        for line in self.lines:
            for c in line:
                self.set_letter_hint(c, UNKNOWN_LETTER)

    def process_hints(self, attempt):
        for letra, dica, in attempt:
            dica_atual = self.get_letter_hint(letra)
            if dica > dica_atual:
                self.set_letter_hint(letra, dica)

    def set_letter_hint(self, letra, dica):
        self.state[letra] = dica

    def get_letter_hint(self, letra):
        return self.state[letra]


    def get_keyboard_lines_with_hints(self):
        res = []
        for linha in self.lines:
            linha_com_dicas = []
            for letra in linha:
                linha_com_dicas.append((letra, self.get_letter_hint(letra)))
            res.append(linha_com_dicas)
        return res
    
    def __iter__(self)->Tuple[str,Hint]:
        for keyline in self.keylines:
            for c in keyline:
                return c, self.get_letter_hint(c) 