from constants import *
from classes import *

def draw_grid(screen):
    for ligne in range(28):
        pygame.draw.line(screen, (255,255,255), (0, TILE_SIZE*ligne), (SCREEN_WIDTH,TILE_SIZE*ligne))
        pygame.draw.line(screen, (255,255,255), (TILE_SIZE*ligne, 0), (TILE_SIZE*ligne, SCREEN_HEIGHT))

def draw_text(texte, font, couleur, x, y, screen):
    img = font.render(texte, True, couleur)
    screen.blit(img, (x, y))

