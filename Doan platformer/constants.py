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

#couleurs-------------------------------------------------------------------------------
clr_white_minus = (155,155,155)
clr_white = (225,225,225)
clr_black = (0,0,0)
clr_red = (255,0,0)
clr_green = (0,255,0)
clr_blue = (0,0,255)
clr_brown = (51,0,17)
#fonts----------------------------------------------------------------------------------
font_bauhaus_40 = pygame.font.SysFont("Bauhaus 93", 40)
font_bauhaus_50 = pygame.font.SysFont("Bauhaus 93", 50)
font_lilitaone_30 = pygame.font.Font("fonts/LilitaOne-Regular.ttf", 30)
font_lilitaone_50 = pygame.font.Font("fonts/LilitaOne-Regular.ttf", 50)
font_lilitaone_60 = pygame.font.Font("fonts/LilitaOne-Regular.ttf", 60)
font_lilitaone_70 = pygame.font.Font("fonts/LilitaOne-Regular.ttf", 70)
font_lilitaone_80 = pygame.font.Font("fonts/LilitaOne-Regular.ttf", 80)
font_ubuntu_30 = pygame.font.Font("fonts/Ubuntu-Regular.ttf", 30)
font_ubuntu_40 = pygame.font.Font("fonts/Ubuntu-Regular.ttf", 40)

