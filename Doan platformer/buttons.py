from constants import *

class Bouton():

    def __init__(self, x, y, width, height, image):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, type, screen):
        if type == 1:
            reset_click = False
            mouse_cos = pygame.mouse.get_pos()
            screen.blit(self.image, self.rect)
            if self.rect.collidepoint(mouse_cos):
                if pygame.mouse.get_pressed()[0] == 1:
                    self.clicked = True
                if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                    reset_click = True
                    self.clicked = False
            return reset_click
        elif type == 2:
            reset_click = False
            mouse_cos = pygame.mouse.get_pos()
            screen.blit(self.image, self.rect)
            if self.rect.collidepoint(mouse_cos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    reset_click = True
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
            return reset_click