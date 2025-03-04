import pygame
from pygame import mixer
import random
from os import path
from pygame.locals import *
import pickle

# GLOBALS -----------------



pygame.init()
pygame.display.set_caption("Doan's Quest")
CLOCK = pygame.time.Clock()
FPS = 60
TILE_SIZE = 50
OFFSET = (pygame.display.Info().current_h - 1000) // TILE_SIZE * (-1) #adaptation to the screen size
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
SCREEN_SCROLL = -7
pygame.quit()