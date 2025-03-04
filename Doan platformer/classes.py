from constants import *


class Fond(pygame.sprite.Sprite):

    def __init__(self, monde):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"sprites\img_background_{monde}.webp").convert()
        self.image = pygame.transform.scale(self.image, (100 * TILE_SIZE, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0

    def update(self, type):
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL // 2
        
fond_group = pygame.sprite.Group()


class Bloc(pygame.sprite.Sprite):

    def __init__(self, x, y, type, monde):
        pygame.sprite.Sprite.__init__(self)
        if path.exists(f"sprites/img_{type}_{monde}.webp"):
            img = pygame.image.load(f"sprites/img_{type}_{monde}.webp")
        else:
            img = pygame.image.load(f"sprites/img_{type}_1.webp")
        if type == "tronc":
            self.image = pygame.transform.scale(img, (50,30))
        else:
            self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, type):
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL

class Bloc_breakable(pygame.sprite.Sprite):

    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        if type == "bloc":
            img = pygame.image.load("sprites\img_breakable_block.webp")
            self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        if type == "platform":
            img = pygame.image.load("sprites\img_platform_break.webp")
            self.image = pygame.transform.scale(img, (TILE_SIZE, 15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.delock = False
        self.counter = 0

    def update(self, type):
        if type == "default":
            if self.delock == True:
                self.counter += 1
                if self.counter >= 7:
                    self.rect.y = 1000
                    self.counter = 0
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL
        if type == "break":
            self.delock = True

bloc_group = pygame.sprite.Group()


class Plateforme(pygame.sprite.Sprite):

    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        if (move_x, move_y) == (1,0):
            img = pygame.image.load("sprites\img_plateforme_xa_1.webp")
        if (move_x, move_y) == (0,1):
            img = pygame.image.load("sprites\img_plateforme_ya_1.webp")
        if (move_x, move_y) == (2,0):
            img = pygame.image.load("sprites\img_plateforme_xb_1.webp")
        if (move_x, move_y) == (0,2):
            img = pygame.image.load("sprites\img_plateforme_yb_1.webp")
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        random_decalage = random.randint(0,70)
        self.rect.x = x - move_x * random_decalage
        self.rect.y = y - move_y * random_decalage
        self.direction = -1
        self.compteur_direction = -70 + random_decalage
        self.move_x = move_x
        self.keep_move_x = move_x
        self.keep_move_y = move_y
        self.move_y = move_y
        self.counter = 0
        self.index = 0
        self.images_right = []
        self.images_left = []
        for i in range(2):
            if (move_x, move_y) == (1,0):
                img_droite = pygame.image.load(f"sprites/img_plateforme_xa_{i + 1}.webp")
            if (move_x, move_y) == (0,1):
                img_droite = pygame.image.load(f"sprites/img_plateforme_ya_{i + 1}.webp")
            if (move_x, move_y) == (2,0):
                img_droite = pygame.image.load(f"sprites/img_plateforme_xb_{i + 1}.webp")
            if (move_x, move_y) == (0,2):
                img_droite = pygame.image.load(f"sprites/img_plateforme_yb_{i + 1}.webp")
            img_droite = pygame.transform.scale(img_droite, (50, 25))
            img_gauche = pygame.transform.flip(img_droite, True, False)
            self.images_right.append(img_droite)
            self.images_left.append(img_gauche)

    def update(self, type):
        if type == "default":
            self.compteur_direction +=1
            if self.compteur_direction > 0:
                self.move_x = 0
                self.move_y = 0
            self.rect.x += self.direction * self.move_x
            self.rect.y += self.direction * self.move_y
            if self.compteur_direction > 60 + 30 * (self.keep_move_x + self.keep_move_y):
                self.move_x = self.keep_move_x
                self.move_y = self.keep_move_y
                self.direction *= -1
                self.compteur_direction = self.compteur_direction * -1 - 50 + 15 * (self.keep_move_x + self.keep_move_y)
            #animation du boug
            animation_cooldown = 3
            self.counter += 1
            if self.counter > animation_cooldown:
                self.counter = 0
                self.index +=1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                if self.direction == 1:
                    self.image = self.images_right[self.index]
        
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL

plateforme_group = pygame.sprite.Group()



#ennemis ---------------------------------------------------------------------------------------------------------------------------------


class Ennemi1a(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_ennemi1a_1.webp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.compteur_direction = 0
        self.counter = 0
        self.index = 0
        self.images_right = []
        self.images_left = []
        for i in range(2):
            img_droite = pygame.image.load(f"sprites/img_ennemi1a_{i + 1}.webp")
            img_droite = pygame.transform.scale(img_droite, (50, 40))
            img_gauche = pygame.transform.flip(img_droite, True, False)
            self.images_right.append(img_droite)
            self.images_left.append(img_gauche)

    def update(self, type):
        if type == "default":
            self.rect.x += self.direction
            self.compteur_direction +=1
            if self.compteur_direction > 40:
                self.direction *= -1
                self.compteur_direction *=-1

            #animation du boug
            animation_cooldown = 3
            self.counter += 1
            if self.counter > animation_cooldown:
                self.counter = 0
                self.index +=1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                if self.direction == 1:
                    self.image = self.images_right[self.index]
        
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL


class Ennemi1b(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_ennemi1b_1.webp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 2
        self.compteur_direction = 0
        self.counter = 0
        self.index = 0
        self.images_right = []
        self.images_left = []
        for i in range(2):
            img_droite = pygame.image.load(f"sprites/img_ennemi1b_{i + 1}.webp")
            img_droite = pygame.transform.scale(img_droite, (50, 40))
            img_gauche = pygame.transform.flip(img_droite, True, False)
            self.images_right.append(img_droite)
            self.images_left.append(img_gauche)

    def update(self, type):
        self.rect.x += self.direction
        self.compteur_direction +=1
        if self.compteur_direction > 60:
            self.direction *= -1
            self.compteur_direction *=-1
        
        #animation du boug
        animation_cooldown = 3
        self.counter += 1
        if self.counter > animation_cooldown:
            self.counter = 0
            self.index +=1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == -2:
                self.image = self.images_left[self.index]
            if self.direction == 2:
                self.image = self.images_right[self.index]
        
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL


class Ennemi2a(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_ennemi2a_1.webp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.compteur_direction = 0
        self.counter = 0
        self.index = 0
        self.images_right = []
        self.images_left = []
        for i in range(2):
            img_droite = pygame.image.load(f"sprites/img_ennemi2a_{i + 1}.webp")
            img_droite = pygame.transform.scale(img_droite, (50, 35))
            img_gauche = pygame.transform.flip(img_droite, True, False)
            self.images_right.append(img_droite)
            self.images_left.append(img_gauche)

    def update(self, type):
        if type == "default":
            animation_cooldown = 3
            self.rect.y += self.direction * 0.8
            self.compteur_direction +=1
            if self.compteur_direction > 60:
                self.direction *= -1
                self.compteur_direction *=-1

            #animation du boug
            self.counter += 1
            if self.counter > animation_cooldown:
                self.counter = 0
                self.index +=1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                if self.direction == 1:
                    self.image = self.images_right[self.index]
        
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL


class Ennemi2b(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_ennemi2b_1.webp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 2
        self.compteur_direction = 0
        self.counter = 0
        self.index = 0
        self.images_right = []
        self.images_left = []
        for i in range(2):
            img_droite = pygame.image.load(f"sprites/img_ennemi2b_{i + 1}.webp")
            img_droite = pygame.transform.scale(img_droite, (50, 35))
            img_gauche = pygame.transform.flip(img_droite, True, False)
            self.images_right.append(img_droite)
            self.images_left.append(img_gauche)

    def update(self, type):
        animation_cooldown = 3
        self.rect.y += self.direction
        self.compteur_direction +=1
        if self.compteur_direction > 60:
            self.direction *= -1
            self.compteur_direction *=-1

        #animation du boug
        self.counter += 1
        if self.counter > animation_cooldown:
            self.counter = 0
            self.index +=1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == -2:
                self.image = self.images_left[self.index]
            if self.direction == 2:
                self.image = self.images_right[self.index]
        
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL


class Ennemi3a(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_ennemi3a_1.webp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = -1
        self.compteur_direction = 0
        self.compteur_tir = 0
        self.counter = 0
        self.index = 0
        self.images_right = []
        self.images_left = []
        self.image_proj = pygame.image.load("sprites/img_bois.webp")
        self.proj_rect = self.image_proj.get_rect()
        for i in range(2):
            img_droite = pygame.image.load(f"sprites/img_ennemi3a_{i + 1}.webp")
            img_droite = pygame.transform.scale(img_droite, (50, 60))
            img_gauche = pygame.transform.flip(img_droite, True, False)
            self.images_right.append(img_droite)
            self.images_left.append(img_gauche)

    def update(self, type):
        if type == "default":
            self.rect.x += self.direction
            if not 165 <= self.compteur_tir < 235:
                self.compteur_direction += 1
            if self.compteur_direction > 40:
                self.direction *= -1
                self.compteur_direction *= -1

            self.compteur_tir += 1
            if self.compteur_tir == 165:
                if self.direction == 1:
                    self.proj_rect.x = self.rect.right
                    self.proj_rect.y = self.rect.y + 30
                if self.direction == -1:
                    self.proj_rect.x = self.rect.left
                    self.proj_rect.y = self.rect.y + 30					
                self.direction_proj = 3 * self.direction
                self.direction_temp = self.direction
                self.direction = 0
            if self.compteur_tir == 235:
                self.direction = self.direction_temp
            if self.compteur_tir > 235:
                self.proj_rect.x += self.direction_proj
                if self.compteur_tir > 300:
                    self.compteur_tir = 0
            #animation du boug
            animation_cooldown = 3
            self.counter += 1
            if self.counter > animation_cooldown:
                self.counter = 0
                self.index +=1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                if self.direction == 1:
                    self.image = self.images_right[self.index]
        
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL


class Ennemi4a(pygame.sprite.Sprite):

    def __init__(self, x, y, lx, ly):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_ennemi2a_1.webp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction_x = 0
        self.direction_y = 0
        self.numero = 0
        self.compteur_direction = 0
        self.counter = 0
        self.index = 0
        self.images_right = []
        self.images_left = []
        self.deplacements = [
            [0,-1,0,1],
            [1,0,-1,0],
            [ly,lx,ly,lx]
        ]
        for i in range(1):
            img_droite = pygame.image.load(f"sprites/img_test.webp")
            img_droite = pygame.transform.scale(img_droite, (50, 35))
            img_gauche = pygame.transform.flip(img_droite, True, False)
            self.images_right.append(img_droite)
            self.images_left.append(img_gauche)

    def update(self, type):
        animation_cooldown = 3
        self.rect.x += self.direction_x
        self.rect.y += self.direction_y
        self.compteur_direction +=1
        if self.compteur_direction > self.deplacements[2][self.numero] * TILE_SIZE:
            self.direction_x = self.deplacements[0][self.numero]
            self.direction_y = self.deplacements[1][self.numero]
            if self.numero < 3:
                self.numero += 1
            else:
                self.numero = 0
            self.compteur_direction = 0

        #animation du boug
        self.counter += 1
        if self.counter > animation_cooldown:
            self.counter = 0
            self.index +=1
            if self.index >= len(self.images_right):
                self.index = 0
            self.image = self.images_left[self.index]
        
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL


class Ennemi5a(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_test.webp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.taille = 50
        self.direction = 1
        self.compteur_direction = 0

    def update(self, type):
        if type == "default":
            if self.direction == 1:
                self.taille = 50
            elif self.direction == -1:
                self.taille = 110
            self.image = pygame.transform.scale(self.image, (self.taille + self.compteur_direction * self.direction, self.taille + self.compteur_direction * self.direction))   
            if self.compteur_direction % 2 == 0:
                self.rect.x -= self.direction
            self.rect.y -= self.direction
            #
            # print(self.rect.x, self.rect.y)
            self.compteur_direction +=1
            if self.compteur_direction > 60:
                self.direction *= -1
                self.compteur_direction = 0
        
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL

ennemi_group = pygame.sprite.Group()


class Pics(pygame.sprite.Sprite):

    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_pics.webp")
        self.image = pygame.transform.scale(self.image, (50, 30))
        if type == "up":
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, type):
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL

pics_group = pygame.sprite.Group()


class Lave(pygame.sprite.Sprite):

    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        if type == "lave":
            self.image = pygame.image.load("sprites\img_lave2_1.webp")
        if type == "lave_full":
            self.image = pygame.image.load("sprites\img_lave_full_1.webp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.index = 0
        self.counter = 0
        self.direction = 1
        self.compteur_direction = 0
        self.images_right = []
        self.images_left = []
        for i in range(2):
            if type == "lave":
                img_droite = pygame.image.load(f"sprites/img_lave2_{i + 1}.webp")
                img_droite = pygame.transform.scale(img_droite, (50, 30))
            if type == "lave_full":
                img_droite = pygame.image.load(f"sprites/img_lave_full_{i + 1}.webp")
                img_droite = pygame.transform.scale(img_droite, (50, 50))
            img_gauche = pygame.transform.flip(img_droite, True, False)
            self.images_right.append(img_droite)
            self.images_left.append(img_gauche)
        
    def update(self, type):  
        if type == "default":
            animation_cooldown = 5
            
            self.counter += 1
            if self.counter > animation_cooldown:
                self.counter = 0
                self.index +=1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                if self.direction == 1:
                    self.image = self.images_right[self.index]  
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL

lave_group = pygame.sprite.Group()


class Firemaker(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_firemaker_off_0.webp")
        self.image = pygame.transform.scale(self.image, (50, 150))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0
        self.counter_onoff = 0
        self.index = 0
        self.index_off = 0
        self.images = []
        self.images_off = []
        self.ison = False
        for i in range(3):
            imgs = pygame.image.load(f"sprites/img_firemaker_on_{i}.webp")
            imgs = pygame.transform.scale(imgs, (50, 150))
            self.images.append(imgs)
        for i in range(2):
            imgs_off = pygame.image.load(f"sprites/img_firemaker_off_{i}.webp")
            imgs_off = pygame.transform.scale(imgs_off, (50, 150))
            self.images_off.append(imgs_off)

    def update(self, type):
        if type == "default":
            #animation du boug
            animation_cooldown = 3
            onoff_cooldown = 300
            self.counter_onoff += 1
            if self.counter_onoff > onoff_cooldown:
                self.counter_onoff = 0
            if self.counter_onoff == 0:
                self.index_off = 0
            if 0 < self.counter_onoff < 180:
                self.counter += 1
                if self.counter > 10 * animation_cooldown:
                    self.counter = 0
                    self.index_off +=1
                    if self.index_off >= len(self.images_off):
                        self.index_off = 0
                self.image = self.images_off[self.index_off]
                self.ison = False
            else:
                self.counter += 1
                self.ison = True
                if self.counter > animation_cooldown:
                    self.counter = 0
                    self.index +=1
                    if self.index >= len(self.images):
                        self.index = 0
                self.image = self.images[self.index]
        
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL

firemaker_group = pygame.sprite.Group()


class Deathwall(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_deathwall.webp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0

    def update(self, type):
        if type == "default":
            self.counter += 1
            if 70 <= self.counter:
                self.rect.x += 5
                self.counter = 70
        
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL


# re-friendly ---------------------------------------------------------------------------------------------------------


class Exit(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("sprites\img_porte_exit.webp")
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE * 2 - 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, type):    
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL

exit_group = pygame.sprite.Group()



class Decoration(pygame.sprite.Sprite):

    def __init__(self, x, y, type, monde):
        pygame.sprite.Sprite.__init__(self)
        if path.exists(f"sprites/img_{type}_{monde}.webp"):
            self.image = pygame.image.load(f"sprites/img_{type}_{monde}.webp")
        else:
            self.image = pygame.image.load(f"sprites/img_{type}_1.webp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, type):
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL

decoration_group = pygame.sprite.Group()
decoration2_group = pygame.sprite.Group()


class Bumper(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_bumper.webp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.index = 0
        self.counter = 0
        self.images = []
        for i in range(3):
            img_droite = pygame.image.load(f"sprites/img_bumper_{i + 1}.webp")
            img_droite = pygame.transform.scale(img_droite, (50, 30))
            self.images.append(img_droite)
    def update(self, type):
        if type == "default":
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL

bumper_group = pygame.sprite.Group()


class Coin(pygame.sprite.Sprite):

    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        if type == "normal":
            img = pygame.image.load("sprites\img_coin.webp")
            self.image = pygame.transform.scale(img, (25, 25))
        if type == "big":
            img = pygame.image.load("sprites\img_big_coin.webp")
            self.image = pygame.transform.scale(img, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self, type):    
        if type == "scroll":
            self.rect.x += SCREEN_SCROLL

coin_group = pygame.sprite.Group()
big_coin_group = pygame.sprite.Group()


groups = [fond_group, ennemi_group, lave_group, pics_group, exit_group, coin_group, bloc_group, plateforme_group, bumper_group, firemaker_group, decoration_group, decoration2_group]
