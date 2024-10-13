class Buffer:
    def __init__(self, max_size: int, accepted_chars: str, initial_char: str = ""):
        self.max_size = max_size
        self.accepted_chars = set(accepted_chars)
        self.initial_char = initial_char
        self.buffer = [self.initial_char] * self.max_size
        self.cursor_position = 0

    def move_cursor_left(self):
        if self.cursor_position > 0:
            self.cursor_position -= 1

    def move_cursor_right(self):
        if self.cursor_position < self.max_size - 1:
            self.cursor_position += 1

    def add_char(self, char: str):
        if char in self.accepted_chars:
            self.buffer[self.cursor_position] = char
            self.move_cursor_right()

    def remove_char(self):
        if self.cursor_position > 0:
            self.move_cursor_left()
            self.buffer[self.cursor_position] = self.initial_char

    def reset(self):
        self.buffer = [self.initial_char] * self.max_size
        self.cursor_position = 0

    def get_current_guess(self) -> str:
        return "".join(self.buffer).strip()

    def __repr__(self):
        return f"Buffer({self.buffer}, cursor_position={self.cursor_position})"
