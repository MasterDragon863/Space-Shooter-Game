import pygame


class Button:
    def __init__(self, x, y, image: pygame.Surface, scale):
        self.x = x
        self.y = y
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self, screen):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        screen.blit(self.image, self.rect.topleft)

        return action


class Slider:
    def __init__(self,pos: tuple, size: tuple, initial_val: float, min: int, max: int):
        self.pos = pos
        self.size = size
        
        self.slider_left = pos[0] - (size[0]//2)
        self.slider_right = pos[0] + (size[0]//2)
        self.slider_top = pos[1] - (size[1]//2)
        
        self.min = min 
        self.max = max
        self.initial_val = (self.slider_right - self.slider_left) * initial_val
        
        self.container_rect = pygame.Rect(self.slider_left, self.slider_top, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left + self.initial_val - 5, self.slider_top, 10, self.size[1])
        
    def update(self, mouse_pos) -> None:
        mouse_click = pygame.mouse.get_pressed()
        if self.container_rect.collidepoint(mouse_pos) and mouse_click[0]:
            self.button_rect.centerx = mouse_pos[0]
        
    def draw(self, surf):
        pygame.draw.rect(surf, (10,10,10), self.container_rect)
        pygame.draw.rect(surf, (252, 127, 3), self.button_rect)
        
    def get_value(self) -> float:
        val_range = self.slider_right - self.slider_left - 1
        button_val = self.button_rect.centerx - self.slider_left
        
        return (button_val/val_range) * (self.max-self.min) + self.min