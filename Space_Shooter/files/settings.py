path = 'D:/saad/GameRelated/Space_Shooter/'
import pygame

from files.func import load_image, load_images, load_sound, debug

from files.Entities import Player

from files.Inanimates import Laser, Asteroid

from files.Interactables import Button, Slider

RES = WIDTH, HEIGHT = 600,600
window = pygame.display.set_mode(RES)
factor = 2
dispaly_res = display_width,display_height = WIDTH//factor, HEIGHT//factor
display = pygame.Surface(dispaly_res)
