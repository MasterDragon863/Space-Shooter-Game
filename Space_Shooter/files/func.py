import pygame
import os

from files.settings import path

os.chdir(f'{path}assets')

pygame.init()

def load_image(image_path: str) -> pygame.Surface:
    return pygame.image.load(image_path).convert_alpha()

def load_images(path: str) -> list[pygame.Surface]:
    return [load_image(os.path.join(path, f)) for f in os.listdir(path) if f.endswith('.png')]

def load_sound(sound_path: str) -> pygame.mixer.Sound:
    return pygame.mixer.Sound(sound_path)

default_font = pygame.font.Font(None, 20)

def debug(
    surf: pygame.Surface,
    info,
    y: int = 10,
    x: int = 10,
    text_color: tuple[int, int, int] = (0, 0, 0),
    bg_color: tuple[int, int, int] = (255, 255, 255),
) -> None:
    """
    Draw debug information on the screen.
    Args:
        surf (pygame.Surface): The surface to draw the debug info onto.
        info (Any): The information to display.
        y (int): The y-coordinate for the debug text.
        x (int): The x-coordinate for the debug text.
        text_color (tuple): RGB color of the text.
        bg_color (tuple): RGB color of the background rectangle.
    """
    font_to_use = default_font
    debug_surf = font_to_use.render(str(info), True, text_color)
    debug_rect = debug_surf.get_rect(topleft=(x, y))

    pygame.draw.rect(surf, bg_color, debug_rect)  # Background for text
    surf.blit(debug_surf, debug_rect)  # Blit the text onto the surface