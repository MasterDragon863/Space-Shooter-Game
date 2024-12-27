import pygame

vector = pygame.math.Vector2

import random


class Laser(pygame.sprite.Sprite):
    def __init__(
        self,
        game,
        image: pygame.Surface,
        x: float,
        y: float,
    ):
        super().__init__()
        self.game = game
        self.image: pygame.Surface = image
        self.rect: pygame.FRect = self.image.get_frect()
        self.rect.center = x, y
        self.velocity: int = 100
        self.mask: pygame.Mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.y -= self.velocity* dt
        if self.rect.bottom < 0 or self.rect.top > self.game.height:
            self.kill()
            
class Asteroid(pygame.sprite.Sprite):
    def __init__(
        self,
        game,
        image: pygame.Surface,
        x: float,
        y: float,):
        super().__init__()
        self.game = game
        self.scale_size = random.randint(16,48)
        self.image: pygame.Surface = image
        self.image: pygame.Surface = pygame.transform.scale(image,(self.scale_size*1.2,self.scale_size) )
        self.rect: pygame.FRect = self.image.get_frect()
        self.rect.topleft = x, y
        self.mask: pygame.Mask = pygame.mask.from_surface(self.image)
        self.velocity = 100
        self.direction = vector(random.randint(-1,1) * random.random(), random.random())
        self.previos_dir = self.direction
        
    def update(self, dt):
        if self.direction.y <= 0.25:
            self.direction.y *= 2
        if self.previos_dir != self.direction:
            self.previos_dir = self.direction
            pygame.transform.rotate(self.image, 90*self.direction.x)
        self.rect.y += self.velocity * dt * self.direction.y
        self.rect.x += self.velocity * dt * self.direction.x
        
        if self.rect.bottom < 0 :
            self.kill()
            
        if self.rect.right>self.game.width:
            self.rect.right = self.game.width
            self.direction.x = -self.direction.x
        
        if self.rect.left<0:
            self.rect.left = 0
            self.direction.x = -self.direction.x    
        
            