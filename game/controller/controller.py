from abc import ABC
import curses


class IControllerCore(ABC):
    def __init__(self) -> None:
        super().__init__()

    def get_input(self):
        pass


class IController(ABC):
    def __init__(self) -> None:
        super().__init__()

    def process_input(self, key: str):
        pass

    def get_input(self):
        pass

    def get_buffer(self):
        pass

    def get_cursor(self):
        pass


class Controller(IController):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.buffer = [""] * 5
        self.cursor_pos = 0
        curses.curs_set(0)  # Hide cursor
        self.stdscr.keypad(True)
        self.run()

    def run(self):
        while True:
            self.stdscr.clear()
            self.display_buffer()
            self.stdscr.refresh()

    def get_input(self):
        key = self.stdscr.getch()
        return self.process_input(key)

    def process_input(self, key):
        if key == curses.KEY_LEFT:
            self.move_cursor_left()
        elif key == curses.KEY_RIGHT:
            self.move_cursor_right()
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return self.submit_buffer()
        elif ord("a") <= key <= ord("z"):
            self.add_letter(chr(key))
        elif key == ord("q"):
            self.quit()

    def move_cursor_left(self):
        if self.cursor_pos > 0:
            self.cursor_pos -= 1
        return self.buffer, self.cursor_pos

    def move_cursor_right(self):
        if self.cursor_pos < 5:
            self.cursor_pos += 1

    def add_letter(self, letter):
        if self.cursor_pos < 5:
            self.buffer[self.cursor_pos] = letter
            self.move_cursor_right()

    def submit_buffer(self):
        if all(self.buffer):
            self.buffer = [""] * 5
            self.cursor_pos = 0


def main(stdscr):
    controller = Controller(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
