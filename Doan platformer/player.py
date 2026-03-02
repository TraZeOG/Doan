import pygame
from assets import *

class Joueur():
    def __init__(self, x, y, numero_joueur, type_level, level):
        self.img = pygame.image.load(f"sprites/img_joueur_{numero_joueur}_0.webp")
        self.reset(x, y, type_level, numero_joueur, level)

    def update(self, game_over, type_level, screen):
        dx = 0
        dy = 0
        walk_cooldown = 5
        if game_over == 0:

            #mouvements du joueur
            if type_level == "speed":
                max_speed = 10
                acceleration = 1
                freinage = 0.8
                self.jump = 19
            elif type_level == "ice":
                max_speed = 7
                acceleration = 0.2
                freinage = 0.1
                self.jump = 19
            elif type_level == "big_jump":
                max_speed = 7
                acceleration = 1
                freinage = 0.8
                self.jump = 29 
            elif type_level == "inversed_controls":
                max_speed = -7
                acceleration = -1
                freinage = 0.8
                self.jump = 19
            elif type_level == "small":
                max_speed = 5
                acceleration = 0.8
                freinage = 0.6
                self.jump = 14
            elif type_level == "big":
                max_speed = 10
                acceleration = 1.2
                freinage = 1
                self.jump = 24
            elif type_level == "snowy_snow":
                max_speed = 8
                self.jump = 19
                acceleration = 0
                freinage = 0
            else:
                max_speed = 7
                acceleration = 1
                freinage = 0.8
                self.jump = 19


            key = pygame.key.get_pressed()
            if type_level == "crossy_road":

                if key[pygame.K_LEFT] and not self.clicked_l and not self.rect.x <= 50 and not self.collision_left:
                    self.rect.x -= 50
                    self.clicked_l = True
                    self.mostleftposition -= 50
                if key[pygame.K_RIGHT] and not self.clicked_r and not self.collision_right:
                    self.rect.x += 50
                    self.clicked_r = True
                    self.mostleftposition += 50
                if key[pygame.K_UP] and not self.clicked_up and not self.clicked_up:
                    self.rect.y -= 50
                    self.clicked_up = True
                if key[pygame.K_DOWN] and not self.clicked_down and not self.collision_down:
                    self.rect.y += 50
                    self.clicked_down = True
                if not key[pygame.K_LEFT]:
                    self.clicked_l = False
                if not key[pygame.K_RIGHT]:
                    self.clicked_r = False
                if not key[pygame.K_UP]:
                    self.clicked_up = False
                if not key[pygame.K_DOWN]:
                    self.clicked_down = False

            elif type_level == "snowy_snow":
                self.vitesse_x = max_speed
            else:
                if key[pygame.K_LEFT]:
                    if not self.vitesse_x <= -1 * max_speed:
                        self.vitesse_x -= acceleration
                    else:
                        self.vitesse_x = - 1 * max_speed
                    self.counter += 1
                    self.direction = -1
                if key[pygame.K_RIGHT]:
                    if not self.vitesse_x >= max_speed:
                        self.vitesse_x += acceleration
                    else:
                        self.vitesse_x = max_speed
                    self.counter += 1
                    self.direction = 1
                if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                    self.counter = 0
                    self.index = 0
                    if self.direction == -1:
                        self.image = self.images_left[self.index]
                    if self.direction == 1:
                        self.image = self.images_right[self.index]

            if type_level == "gliding":
                if key[pygame.K_SPACE] and not self.en_saut and self.vitesse_fin_y > -14:
                    self.vitesse_y = -15
                    self.airtime = True
                    if self.vitesse_fin_y == 0:
                        jump_msc.play()
                    self.vitesse_fin_y -= 3
                    if self.vitesse_fin_y <= -14:
                        self.en_saut = True
                        self.vitesse_fin_y = 0
                if key[pygame.K_SPACE] == False and self.airtime:
                    self.en_saut = True
                    self.vitesse_y = 2
                    self.vitesse_fin_y = 0
                if not self.airtime:
                    self.en_saut = False
                    self.vitesse_fin_y = 0

            elif type_level == "flappy_bird":
                if key[pygame.K_SPACE] and not self.en_saut:
                    jump_msc.play()
                    self.vitesse_y = -15
                    self.en_saut = True
                if not key[pygame.K_SPACE]:
                    self.en_saut = False

            elif type_level == "crossy_road":
                pass

            elif type_level == "kangourou":
                if not self.airtime:
                    self.vitesse_y = -20
                    jump_msc.play()
                    self.airtime = True

            else:
                if key[pygame.K_SPACE] and not self.en_saut and self.vitesse_fin_y < 14:
                    if 0 <= self.vitesse_fin_y < 6:
                        self.vitesse_y = - 1 * self.jump
                    if 6 <= self.vitesse_fin_y < 12:
                        self.vitesse_y = - 1 * self.jump + 3
                    if 12 <= self.vitesse_fin_y <= 14:
                        self.vitesse_y = - 1 * self.jump + 8
                    if self.vitesse_fin_y == 0:
                        jump_msc.play()
                    self.vitesse_fin_y += 2
                    self.airtime = True
                    if self.vitesse_fin_y <= -14:
                        self.en_saut = True
                        self.vitesse_fin_y = 0
                if not key[pygame.K_SPACE] and self.airtime and not self.en_saut:
                    self.en_saut = True
                    if self.vitesse_y < -9:
                        self.vitesse_y = -9
                    self.vitesse_fin_y = 0
                if not self.airtime:
                    self.en_saut = False
                    self.vitesse_fin_y = 0


            #animation du joueur
            if not self.vitesse_y < 0:
                if self.image == self.image_saut:
                    self.image = self.images_right[0]
                self.airtime = True
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index +=1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                if self.direction == 1:
                    self.image = self.images_right[self.index]
            if self.vitesse_y < 0:
                if self.direction == 1:
                    self.image = self.image_saut
                else:
                    self.image = pygame.transform.flip(self.image_saut, True, False)

            #la gravité c'est utile
            #gravité y
            if type_level == "crossy_road":
                pass

            else:
                if self.vitesse_y > 20:
                    self.vitesse_y = 20
                else:
                    self.vitesse_y +=1
                dy += self.vitesse_y	
                #gravité x
                if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                    if self.vitesse_x > 1:
                        self.vitesse_x -= freinage
                        if self.vitesse_x > 7:
                            self.vitesse_x = 7
                    elif self.vitesse_x < -1:
                        self.vitesse_x += freinage
                        if self.vitesse_x < -7:
                            self.vitesse_x = -7
                    else:
                        self.vitesse_x = 0
                dx += int(self.vitesse_x)
                        


            if type_level == "crossy_road":
                for bloc in bloc_group:
                    #collisions en y
                    if bloc.rect.colliderect(self.rect.x, self.rect.y + 50, self.width, self.height):
                        self.collision_down = True
                    else:
                        self.collision_down = False
                    if bloc.rect.colliderect(self.rect.x, self.rect.y - 50, self.width, self.height):
                        self.collision_up = True
                    else:
                        self.collision_up = False
                    if bloc.rect.colliderect(self.rect.x + 50, self.rect.y, self.width, self.height):
                        self.collision_right = True
                    else:
                        self.collision_right = False
                    if bloc.rect.colliderect(self.rect.x - 50, self.rect.y, self.width, self.height):
                        self.collision_left = True
                    else:
                        self.collision_left = False     
            
            else:

                for bloc in bloc_group:
                    #collisions en y
                    if bloc.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.vitesse_y < 0:
                            dy= bloc.rect.bottom - self.rect.top
                            self.vitesse_y = 0
                        elif self.vitesse_y >= 0:
                            dy= bloc.rect.top - self.rect.bottom
                            self.vitesse_y = 0
                            self.airtime = False
                            bloc.update("break")
                    #collisions en x
                    if bloc.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx= 0
                        self.vitesse_x = 0

            #collisions avec chaque groupe d'ennemis

            if pygame.sprite.spritecollide(self, ennemi_group, False):
                game_over= -1
            if pygame.sprite.spritecollide(self, pics_group, False):
                game_over= -1
            if pygame.sprite.spritecollide(self, lave_group, False):
                game_over= -1
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            for platform in plateforme_group:
                #collisions en y
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.airtime == False and self.rect.y > platform.rect.y:
                        if platform.rect.colliderect(self.rect.x, self.rect.y + 10, self.width, self.height):
                            game_over = -1
                    else:
                        if self.vitesse_y < 0:
                            dy= platform.rect.bottom - self.rect.top
                            self.vitesse_y = 0
                        elif self.vitesse_y >= 0:
                            dy= platform.rect.top - self.rect.bottom
                            self.vitesse_y = 0
                            self.airtime = False
                        if platform.move_x != 0:
                            self.rect.x += platform.move_x * platform.direction
                #collisions en x
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx= 0
                    self.vitesse_x = 0

            for bumper in bumper_group:
                #collisions en y
                if bumper.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    self.vitesse_y = -23
                    for _ in range(5):
                        bumper_group.update("default")
                #collisions en x
                if bumper.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and not bumper.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    dx= 0
                    self.vitesse_x = 0

            for firemaker in firemaker_group:
                if firemaker.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height) and firemaker.ison == True:
                    game_over = -1

            #update des coordonnées du joueur
            self.rect.x += dx
            self.mostleftposition += dx
            self.rect.y += dy

        elif game_over == -1:
            if not self.lock:
                self.lock = True
                self.y_temp = self.rect.y
            self.image = self.image_dead
            if abs(self.rect.y - self.y_temp) < 150:
                self.rect.y -= 5


        if type_level == "small":
            self.image = pygame.transform.scale(self.image, (30,60))
        if type_level == "flappy_bird":
            self.image = pygame.transform.scale(self.image, (50,50))
        if type_level == "crossy_road":
            self.image = pygame.transform.scale(self.image, (49,49))
        if type_level == "big":
            self.image = pygame.transform.scale(self.image, (80,140))        

        #on blit le joueur sur le screen hein (parce que sinon il est invisible est c'est compliqué de jouer)
        screen.blit(self.image, self.rect)

        return game_over
    
    
    def reset(self, x, y, type_level, numero_joueur, level):

        self.image = pygame.image.load(f"sprites/img_joueur_{numero_joueur}_0.webp")
        self.image_dead = pygame.image.load("sprites/img_dead_joueur.webp")
        self.image_saut = pygame.image.load(f"sprites/img_joueur_{numero_joueur}_jump.webp")
        if type_level == "small":
            self.image = pygame.transform.scale(self.image, (30,60))
        if type_level == "flappy_bird":
            self.image = pygame.transform.scale(self.image, (50,50))
        if type_level == "crossy_road":
            self.image = pygame.transform.scale(self.image, (48,48))
        if type_level == "big":
            self.image = pygame.transform.scale(self.image, (80,140))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vitesse_y = 0
        self.vitesse_x = 0
        self.en_saut = False
        self.airtime = False
        self.vitesse_fin_y = 0
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.direction = 1
        if type_level == "snowy_snow":
            self.direction = 0
        self.mostleftposition = 0
        self.lock = False
        self.gliding = False
        if level == 10 or level == 19:
            self.gliding = True
        else:
            self.gliding = False


        for i in range(4):
            img_droite = pygame.image.load(f"sprites/img_joueur_{numero_joueur}_{i}.webp")
            img_gauche = pygame.transform.flip(img_droite, True, False)
            self.images_right.append(img_droite)
            self.images_left.append(img_gauche)