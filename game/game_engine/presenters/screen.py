from abc import ABC, abstractmethod
from typing import Iterator, List, Tuple

from game.game_engine.presenters.colored_string import ColoredString


class IScreen(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, colored_string: ColoredString, pos: Tuple[int, int]):
        pass

    @abstractmethod
    def merge(self, other: object):
        pass

    @abstractmethod
    def __iter__(self):
        pass
    @abstractmethod
    def __eq__(self, value: object) -> bool:
        pass
    @abstractmethod
    def __str__(self) -> str:
        pass


class Screen(IScreen):
    def __init__(self) -> None:
        self.strings: List[Tuple[ColoredString, Tuple[int,int]]] = []

    def add(self, colored_string: ColoredString, pos: Tuple[int, int]) -> None:
        self.strings.append((colored_string, pos))

    def merge(self, other):
        if isinstance(other, self.__class__):
            self.strings += other.strings

    def __iter__(self) -> Iterator[Tuple[ColoredString, Tuple[int, int]]]:
        for string, pos in self.strings:
            yield string, pos

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            if len(self.strings) != len(other.strings):
                print(f"len diverges {len(self.strings)} vs {len(other.strings)}")
                return False
            for (stringA, posA), (stringB, posB) in zip(self.strings, other.strings):
                if posA != posB:
                    print(f"pos A and B diverges: {posA} vs {posB}")
                    return False
                if stringA != stringB:
                    print(f"strings A and B diverges: {stringA} vs {stringB}")
                    return False
            return True

        print("not same class")
        return False

    def __str__(self) -> str:
        res = ""
        for colored_string, pos in self.strings:
            res += colored_string.str + " " + str(colored_string.colors)
        return res
