from game.viewer.screen import Screen
from game.viewer.colored_string import ColoredString
from game.viewer.terminal_manipulator import IDisplayCore
import pygame
from typing import Tuple


UNDERLINE = 3
ENDC = 4
COR_ERRADO = 0
COR_CERTO = 1
COR_POSICAO = 2


pygame_color_dict = {
    COR_ERRADO: (0, 0, 0),  # Light Red
    COR_CERTO: (20, 180, 20),  # Green
    COR_POSICAO: (180, 180, 0),  # Yellow
    ENDC: (0, 0, 0),  # White (used for resetting color in terminal)
    UNDERLINE: (
        0,
        0,
        0,
    ),  # White (no direct underline support in Pygame, so using white)
}


class PygameCore(IDisplayCore):
    def __init__(
        self, color_dict, screen_size=(800, 800), font_size=64, bg_color=(0, 0, 0)
    ) -> None:
        super().__init__()
        pygame.init()
        self.color_dict = color_dict
        self.screen_size = screen_size
        self.bg_color = bg_color
        self.font_size = font_size
        self.screen = pygame.display.set_mode(screen_size)
        self.font = pygame.font.Font(None, font_size)
        self.screen.fill(bg_color)
        pygame.display.flip()

    def print_colored_string(self, colored_string: ColoredString, pos: Tuple[int, int]):
        x, y = (pos[1] * self.font_size, pos[0] * self.font_size)
        print(f"{colored_string}\nX, Y = ", x, y)
        for letter, color, _ in colored_string:
            color_rgb = self.color_dict[color]
            text_surface = self.font.render(letter, True, (255, 255, 255), color_rgb)
            self.screen.blit(text_surface, (x, y))
            x += text_surface.get_width()
        pygame.display.flip()

    def clear_line(self, n: int) -> None:
        y = n * self.font_size
        clear_rect = pygame.Rect(0, y, self.screen_size[0], self.font_size)
        self.screen.fill(self.bg_color, clear_rect)
        pygame.display.flip()

    def print_screen(self, screen: Screen):
        self.screen.fill(self.bg_color)
        for colored_string, pos in screen:
            self.print_colored_string(colored_string, pos)
        pygame.display.flip()
