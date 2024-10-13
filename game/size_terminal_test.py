import sys
import signal
import termios
import fcntl
import struct


def get_terminal_size():
    """Get the current size of the terminal window."""
    h, w, hp, wp = struct.unpack(
        "HHHH",
        fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, struct.pack("HHHH", 0, 0, 0, 0)),
    )
    return w, h


def print_terminal_size():
    """Print the current terminal size."""
    w, h = get_terminal_size()
    print(f"Terminal size: {w} columns, {h} rows")


def handle_resize(signum, frame):
    """Handle the window resize signal."""
    print_terminal_size()


def main():
    """Main function to monitor terminal size changes."""
    # Register the signal handler for SIGWINCH (window size change)
    signal.signal(signal.SIGWINCH, handle_resize)

    print("Monitoring terminal size changes. Resize the window to see updates.")
    print_terminal_size()  # Print the initial size

    # Keep the script running to monitor changes
    try:
        while True:
            signal.pause()  # Wait for a signal to arrive
    except KeyboardInterrupt:
        print("\nExiting.")


if __name__ == "__main__":
    main()
