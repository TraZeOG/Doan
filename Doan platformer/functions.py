from constants import *
from classes import *

def draw_grid(screen):
    for ligne in range(28):
        pygame.draw.line(screen, (255,255,255), (0, TILE_SIZE*ligne), (SCREEN_WIDTH,TILE_SIZE*ligne))
        pygame.draw.line(screen, (255,255,255), (TILE_SIZE*ligne, 0), (TILE_SIZE*ligne, SCREEN_HEIGHT))

def draw_text(texte, font, couleur, x, y, screen):
    img = font.render(texte, True, couleur)
    screen.blit(img, (x, y))

def human_delay():
    pygame.time.delay(20)
    
def full_draw(groups, screen):
    for group in groups:
        group.draw(screen)

def full_update(groups):
    for group in groups:
        group.update("default")

def full_scroll(groups):
    for group in groups:
        group.update("scroll")

def write(base, font1, font2, font3, color, message, max_length, screen):
    if not base == "[pas de nom]":
        text = f"{base}"
    else:
        text = ""
    writing = True
    while writing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    writing = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < max_length:
                        text += event.unicode
        screen.fill((30, 30, 30))
        text_width, text_height = font1.size(message)
        draw_text(message, font1, clr_white, (SCREEN_WIDTH - text_width) // 2, (SCREEN_HEIGHT - text_height) // 2 - 100, screen)
        draw_text("press Enter to finish", font3, color, SCREEN_WIDTH - 300, SCREEN_HEIGHT - 50, screen)
        text_width, text_height = font2.size(text)
        draw_text(text, font2, clr_white, (SCREEN_WIDTH - text_width) // 2, (SCREEN_HEIGHT - text_height) // 2, screen)
        pygame.display.flip()
        CLOCK.tick(30)
    return text