import os
import select
import sys
import tty
import termios
import fcntl
import struct
import signal
from collections import deque

# ANSI codes for clearing and cursor manipulation
CLEAR_SCREEN = "\033[2J"
CURSOR_HOME = "\033[H"


class TerminalUI:
    def __init__(self):
        self.lines = deque()  # Store the lines for scrolling
        self.scroll_pos = 0  # Scroll position
        self.height, self.width = self.get_terminal_size()
        self.keep_running = True

        # Setup input for raw mode
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())

        # Handle window resize
        signal.signal(signal.SIGWINCH, self.on_resize)

    def get_terminal_size(self):
        """Get the current size of the terminal window."""
        h, w, _, _ = struct.unpack(
            "HHHH",
            fcntl.ioctl(
                sys.stdout, termios.TIOCGWINSZ, struct.pack("HHHH", 0, 0, 0, 0)
            ),
        )
        return h, w

    def on_resize(self, signum, frame):
        """Handle the window resize event."""
        self.height, self.width = self.get_terminal_size()
        self.render()

    def render(self):
        """Render the visible part of the buffer on the screen."""
        os.system("clear")  # Clear the screen

        # Calculate the visible window of the buffer
        start_line = max(0, self.scroll_pos)
        end_line = min(len(self.lines), self.scroll_pos + self.height)

        # Print the visible lines
        for i in range(start_line, end_line):
            print(self.lines[i][: self.width], self.scroll_pos)

        # If there are fewer lines than the screen height, fill the rest with blank lines
        for _ in range(end_line - start_line, self.height):
            print("")
        sys.stdout.flush()

    def add_line(self, line):
        """Add a new line to the buffer and scroll if needed."""
        self.lines.append(line)
        # if len(self.lines) > self.height:
        #    self.scroll_pos += (
        #        1  # Auto-scroll when the buffer exceeds the screen height
        #    )

    def handle_input(self):
        """Handle keyboard input and scrolling."""
        while self.keep_running:
            # Use os.read for non-blocking key input
            key = os.read(sys.stdin.fileno(), 1).decode("utf-8")

            if key == "\x03":  # Ctrl+C to exit
                self.keep_running = False
                self.exit_gracefully()
            elif key == "\x1b[A":  # Up arrow
                self.scroll_up()
            elif key == "\x1b[B":  # Down arrow
                self.scroll_down()
            else:
                print("NONE KEY")

            # Redraw after handling input
            self.render()

    def scroll_up(self):
        """Scroll up the buffer."""
        if self.scroll_pos > 0:
            self.scroll_pos -= 1

    def scroll_down(self):
        """Scroll down the buffer."""
        if self.scroll_pos + self.height < len(self.lines):
            self.scroll_pos += 1

    def exit_gracefully(self):
        """Restore terminal settings and exit."""
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
        sys.stdout.write("\033[?25h")  # Show cursor
        sys.stdout.write("\033[2J")  # Clear the entire screen
        sys.stdout.write("\033[H")
        sys.stdout.flush()
        os.system("clear")
        print("BYE")

    def isData(self, block=True):
        if block:
            return select.select([sys.stdin], [], []) == ([sys.stdin], [], [])
        else:
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    def get_input(self):
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            print("\033[?25l", end="")
            sys.stdout.flush()
            tty.setcbreak(sys.stdin.fileno())

            while 1:
                if self.isData():
                    k = os.read(sys.stdin.fileno(), 1).decode("utf-8")
                    print("k:", k.encode("utf-8"), ord(k))
                    if k == "Q":
                        exit(0)
                    elif k == "\x1b":
                        print("waiting for data")
                        is_data = self.isData(0)
                        print("ISDATA:", is_data)
                        if is_data:
                            kk = os.read(sys.stdin.fileno(), 2).decode("utf-8")
                            print(
                                "ó o print:", kk.encode("utf-8"), ord(kk[0]), ord(kk[1])
                            )
                            if kk == "[C":
                                print("RIGHTARROW")
                            elif kk == "[D":
                                print(" LEFTARROW")
                        else:
                            print("ESC")

        finally:

            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            sys.stdout.write("\033[?25h")


# Example Usage
if __name__ == "__main__":
    ui = TerminalUI()

    # Add some dummy lines to the buffer
    for i in range(100):
        ui.add_line(f"Line {i}")

    ui.render()
    try:
        ui.handle_input()
    except KeyboardInterrupt:
        ui.exit_gracefully()
