import pygame

from files.Inanimates import Laser

pygame.init()

vector = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game, image: pygame.Surface, x: int, y: int) -> None:
        super().__init__()  # Correctly initialize the Sprite base class
        self.game = game  # Store a reference to the game object
        self.image = pygame.transform.scale2x(image)  # Assign the player image
        self.rect: pygame.FRect = (
            self.image.get_frect()
        )  # Define the player's bounding rectangle
        self.rect.midbottom = (x, y)  # Set the initial position
        self.mask: pygame.Mask = pygame.mask.from_surface(
            self.image
        )  # Create a mask for pixel-perfect collisions
        self.speed: int = 100  # Set the player's movement speed

        self.pos = vector(x, y)
        self.can_shoot: bool = True
        self.shoot_time = 0
        self.current_time = 0
        self.cooldown_time = 2000
        # self.acceleration  = vector(0,0)
        # self.velocity = vector(0,0)

        # self.friction = 2

    def move(self, dt):
        # self.acceleration  = vector(0,0)
        # Move the player based on user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 2:
            # self.acceleration.y = -self.speed * dt
            self.pos.y -= self.speed * dt
        if keys[pygame.K_DOWN] and self.rect.bottom < self.game.height:
            # self.acceleration.y = self.speed *dt
            self.pos.y += self.speed * dt
        if keys[pygame.K_RIGHT] and self.rect.right < self.game.width:
            # self.acceleration.x = self.speed *dt
            self.pos.x += self.speed * dt
        if keys[pygame.K_LEFT] and self.rect.left > 1:
            # self.acceleration.x = -self.speed *dt
            self.pos.x -= self.speed * dt

        # self.acceleration.x = min(self.acceleration.x,2)
        # self.acceleration.y = min(self.acceleration.y,2)

        # self.acceleration.x -= self.velocity.x * self.friction * dt
        # self.acceleration.y -= self.velocity.y * self.friction * dt
        # self.velocity += self.acceleration
        # self.pos += self.velocity + 0.5*self.acceleration

        self.rect.midbottom = self.pos   
        
    def shoot(self,dt) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.game.effects_channel.play(self.game.assets['laser-sound'], loops=0)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.image = pygame.transform.scale2x(self.game.assets['player_images'][1])
            laser = Laser(self.game, self.game.assets['laser'], self.rect.midtop[0] ,self.rect.midtop[1])
            self.game.all_sprite.add(laser)
            self.game.lasers.add(laser)
                        

    def cooldown(self):
        if not self.can_shoot:
            self.current_time = pygame.time.get_ticks()
            if (self.current_time - self.shoot_time) >= self.cooldown_time:
                self.can_shoot = True
                self.image = pygame.transform.scale2x(self.game.assets['player_images'][0])
            if  2 * self.cooldown_time//3 >(self.current_time - self.shoot_time) >= self.cooldown_time//3: 
                self.image = pygame.transform.scale2x(self.game.assets['player_images'][2])
            if  self.cooldown_time >(self.current_time - self.shoot_time) >= 2 *self.cooldown_time//3: 
                self.image = pygame.transform.scale2x(self.game.assets['player_images'][3])
                
            
    
    def update(self, dt) -> None:
        self.move(dt)
        self.shoot(dt)
        self.cooldown()
