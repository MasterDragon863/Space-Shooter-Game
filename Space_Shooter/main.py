import pygame
import random
from files.settings import *

pygame.init()


class Game(object):
    def __init__(
        self, display: pygame.Surface, window: pygame.Surface, width: int, height: int
    ) -> None:
        self.dis = display
        self.window = window
        self.width = width
        self.height = height
        self.running_game = True
        self.clock = pygame.time.Clock()
        self.score = 0
        self.font = pygame.font.Font(None, 32)

        self.volume = 1
        self.music = 1
        pygame.mixer.set_num_channels(3)
        self.music_channel = pygame.mixer.Channel(0)
        self.effects_channel = pygame.mixer.Channel(1)
        self.game_music = pygame.mixer.Channel(2)
        
        self.volume_slider = Slider((320, 260), (400, 40), 1, 0, 1)
        self.music_slider = Slider((320, 360), (400, 40), 1, 0, 1)
        self.difficulty_slider = Slider((320, 460), (400, 40), 0.5, 1, 10)

        self.assets: dict = {
            "ship": load_image("player/Ship_1.png"),
            "player_images": load_images("player"),
            "laser": load_image("bullet.png"),
            "star": load_image("star.png"),
            "asteroid": pygame.transform.scale2x(load_image("asteroid.png")),
            "play": pygame.transform.scale(load_image("buttons/play.png"), (224, 64)),
            "quit": pygame.transform.scale(load_image("buttons/quit.png"), (224, 64)),
            "options": pygame.transform.scale(
                load_image("buttons/options.png"), (224, 64)
            ),
            "back": pygame.transform.scale(load_image("buttons/back.png"), (64, 64)),
            "pause": pygame.transform.scale(load_image("buttons/pause.png"), (64, 64)),
            "rerun": pygame.transform.scale(load_image("buttons/rerun.png"), (64, 64)),
            "laser-sound": load_sound("audio/laser.mp3"),
            "explosion": load_sound("audio/explosion.wav"),
            "menu-music": load_sound("audio/menu-music.mp3"),
            "game-music": load_sound("audio/game-music.mp3"),
            "button-click": load_sound("audio/button-click.mp3"),
            "game-over": load_sound("audio/game-over.mp3"),
        }
        self.assets["laser-sound"].set_volume(0.5 * self.volume)
        self.assets["asteroid"].set_colorkey((255, 255, 255))  # type: ignwindow
        self.assets["play"].set_colorkey((255, 255, 255))  # type: ignore
        self.assets["quit"].set_colorkey((255, 255, 255))  # type: ignore
        self.assets["options"].set_colorkey((255, 255, 255))  # type: ignore
        self.assets["back"].set_colorkey((255, 255, 255))  # type: ignore
        self.assets["pause"].set_colorkey((255, 255, 255))  # type: ignore
        self.assets["rerun"].set_colorkey((255, 255, 255))  # type: ignore

        self.all_sprite = pygame.sprite.Group()
        self.player = Player(
            self, self.assets["player_images"][0], self.width // 2, self.height  # type: ignore
        )
        self.lasers = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.all_sprite.add(self.player)
        self.font = pygame.font.Font("Tiny5-Regular.ttf", 20)

        self.transfer = "menu"
        self.state = "menu"
        
        self.difficulty = 5
        
        with open(f"{path}files/highscores.txt", "r") as f:
            self.line = f.readlines()[-1]
            self.line = self.line.strip('\n')
            self.highscore = int(self.line)

    def __handle_events(
        self,
    ) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running_game = False
                pygame.quit()
                exit()

    def __random_positions(self, amount: int = 40) -> list[tuple[int, int]]:
        rand_pos: list[tuple[int, int]] = []
        for _ in range(amount):
            pos: tuple[int, int] = (
                random.randint(0, (self.width - 16) // 10) * 10,
                random.randint(0, (self.height - 16) // 10) * 10,
            )
            rand_pos.append(pos)

        return rand_pos

    def __add_asteroids(self, amount: int = 5) -> None:
        positions = self.__random_positions(amount)
        for pos in positions:
            asteroid = Asteroid(
                self, self.assets["asteroid"], pos[0], -30
            )  # type:ignore
            self.all_sprite.add(asteroid)
            self.asteroids.add(asteroid)

    def game_over(self):
        
        font = pygame.font.Font("Tiny5-Regular.ttf", 65)
        font2 = pygame.font.Font("Tiny5-Regular.ttf", 50)
        once = False
        while True:
            self.assets["button-click"].set_volume(0.5 * self.volume)
            self.window.fill((30, 30, 30))
            self.__handle_events()

            text1 = font.render("Game Over", True, "White")
            self.window.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - text1.get_height() // 2 - 125))  # type: ignore
            if self.score <= int(self.highscore):
                text2 = font.render(f"Score: {self.score}", True, "White")
                text3 = font2.render(f"You didn't defeat \nThe highscore: \n({self.highscore})", True, "White")
                self.window.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - text2.get_height() // 2 - 50))  # type: ignore
                self.window.blit(text3, (WIDTH // 2 - text2.get_width() // 2 - 70, HEIGHT // 2 - text2.get_height() // 2 + 25))  # type: ignore
                quit = Button(WIDTH // 2 + 32, 480, self.assets["quit"], 1)
                rerun = Button(WIDTH // 2 , 550, self.assets["rerun"], 1)
            else:
                text2 = font.render(f"New Highscore! ({self.score})", True, "White")
                self.window.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - text2.get_height() // 2 - 50))   
                if not once:
                    with open(f"{path}files/highscores.txt", "a") as f:
                        f.write(f"{self.score}\n")
                        once = True
                quit = Button(WIDTH // 2 + 32, 400, self.assets["quit"], 1)
                rerun = Button(WIDTH // 2, 450, self.assets["rerun"], 1)
                
                
            if rerun.draw(self.window):
                self.effects_channel.play(self.assets["button-click"], loops=0)
                self.score = 0
                self.running_game = True
                for asteroid in self.asteroids:
                    asteroid.kill()
                    
                for laser in self.lasers:
                    laser.kill()
                with open(f"{path}files/highscores.txt", "r") as f:
                    self.line = f.readlines()[-1]
                    self.highscore = int(self.line.strip('\n'))
                    
                self.run_game()
                
                break    
                
            if quit.draw(self.window):
                self.effects_channel.play(self.assets["button-click"], loops=0)
                pygame.time.delay(200)
                pygame.quit()
                break

            pygame.display.update()

    def run_game(
        self,
    ) -> None:
        star_pos = self.__random_positions()
        self.spawn_time = pygame.time.get_ticks()
        pause = Button(550, 32, self.assets["pause"], 1)
        while self.running_game:
            self.assets["game-music"].set_volume(0.1 * self.music)
            self.assets["laser-sound"].set_volume(0.5 * self.volume)
            self.assets["explosion"].set_volume(0.5 * self.volume)
            self.assets["game-music"].play(-1)
            self.assets["menu-music"].stop()
            self.dis.fill((30, 30, 30))
            self.dt = self.clock.tick() / 1000
            self.__handle_events()
            for pos in star_pos:
                self.dis.blit(self.assets["star"], pos)  # type:ignore

            if pygame.time.get_ticks() - self.spawn_time >= 3000:
                self.__add_asteroids(self.difficulty)
                self.spawn_time = pygame.time.get_ticks()
            self.all_sprite.update(self.dt)
            score_text = self.font.render(f"SCORE: {self.score}", True, "white")
            self.dis.blit(score_text, (10, 10))  # type: ignore
            self.all_sprite.draw(self.dis)
            highscore = self.font.render(f"HIGHSCORE: {self.highscore}", True, "white")
            self.dis.blit(highscore, (10, 30))  # type: ignore

            asteroid: Asteroid
            for asteroid in self.asteroids:
                if pygame.sprite.spritecollide(
                    asteroid, self.lasers, True, pygame.sprite.collide_mask
                ):
                    if asteroid.scale_size <= 24:
                        self.score += 13
                    elif asteroid.scale_size <= 32:
                        self.score += 9
                    elif asteroid.scale_size <= 40:
                        self.score += 5
                    else:
                        self.score += 3

                    self.effects_channel.play(self.assets["explosion"], loops=0)
                    asteroid.kill()

            self.window.blit(
                pygame.transform.scale(
                    self.dis, (self.window.get_width(), self.window.get_height())
                )
            )
            if pygame.sprite.spritecollide(
                self.player, self.asteroids, False, pygame.sprite.collide_mask
            ):

                self.assets["game-music"].stop()
                self.music_channel.play(self.assets["game-over"], loops=0)
                self.game_over()
                self.running_game = False
                break

            if pause.draw(self.window):
                self.effects_channel.play(self.assets["button-click"], loops=0)
                self.transfer = "game"
                self.state = "option"
                self.menu()

            pygame.display.update()

    def menu(
        self,
    ) -> None:
        font1 = pygame.font.Font("Tiny5-Regular.ttf", 75)
        play = Button(WIDTH // 2 + 25, 250, self.assets["play"], 1)
        quit = Button(WIDTH // 2 + 25, 450, self.assets["quit"], 1)
        options = Button(WIDTH // 2, 350, self.assets["options"], 1)
        back = Button(32, 32, self.assets["back"], 1)
        while True:
            self.assets["menu-music"].set_volume(0.1 * self.music)
            self.assets["button-click"].set_volume(1 * self.volume)
            self.assets["game-music"].set_volume(0.1 * self.music)
            self.assets["menu-music"].play(-1)
            self.assets["game-music"].stop()

            self.window.fill((30, 30, 30))
            dt = self.clock.tick() / 1000
            self.__handle_events()

            if self.state == "menu":
                text = font1.render("Space Invaders", True, ("White"))
                self.window.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))
                if play.draw(self.window):
                    self.effects_channel.play(self.assets["button-click"], loops=0)
                    self.assets["menu-music"].stop()
                    app.run_game()
                    break
                if quit.draw(self.window):
                    self.effects_channel.play(self.assets["button-click"], loops=0)
                    pygame.quit()
                    break

                if options.draw(self.window):
                    self.effects_channel.play(self.assets["button-click"], loops=0)
                    self.state = "option"

            if self.state == "option":
                mouse_pos = pygame.mouse.get_pos()
                text = font1.render("Options", True, ("White"))
                self.window.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))

                font2 = pygame.font.Font("Tiny5-Regular.ttf", 30)

                if back.draw(self.window):
                    if self.transfer == "menu":
                        self.effects_channel.play(self.assets["button-click"], loops=0)
                        self.state = "menu"
                    else:
                        break

                text = font2.render("Sound Effects:", True, ("White"))
                self.window.blit(text, (250, 210))
                self.volume_slider.draw(self.window)
                self.volume_slider.update(mouse_pos)
                self.volume = self.volume_slider.get_value()
                text = font2.render("Music:", True, ("White"))
                self.window.blit(text, (250, 310))
                self.music_slider.draw(self.window)
                self.music_slider.update(mouse_pos)
                self.music = self.music_slider.get_value()
                text = font2.render("Difficulty:", True, ("White"))
                self.window.blit(text, (250, 410))
                self.difficulty_slider.draw(self.window)
                self.difficulty_slider.update(mouse_pos)
                self.difficulty = int(self.difficulty_slider.get_value())

            pygame.display.update()


if __name__ == "__main__":
    app = Game(display, window, display_width, display_height)
    app.menu()
