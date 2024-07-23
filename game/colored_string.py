class ColoredString:
    def __init__(self, string, colors) -> None:
        self.str = string
        self.colors = colors

    def __iter__(self):
        for pos, letter_and_color in enumerate(zip(self.str, self.colors)):
            yield letter_and_color[0], letter_and_color[1], pos

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            for valuesA, valuesB in zip(self, other):
                letterA = valuesA[0]
                letterB = valuesB[0]
                if letterA != letterB:
                    return False
                colorA = valuesA[1]
                colorB = valuesB[1]
                if colorA != colorB:
                    return False
            return True
        return False
