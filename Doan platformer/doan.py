from imports import *

#variables------------------------------------------------------------------------------



pygame.init()
SCREEN = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#init mixer
mixer.pre_init(44100, 16, 2, 4096)
mixer.init()

pickle_in = open(f'data/data_main', 'rb')
datas = pickle.load(pickle_in)
#factory settings 
datas = [0,1,1,11,[0,0,10,10,100,150,200,250,300,350,999], ["[pas de nom]"] * 20]

game_over = 0
level = 1
monde = 1

type_level = "normal"

nb_levels = 36
nb_levels_main_quest = 21
nb_minis_jeux = 16
nb_skins = 11
nb_created_levels = datas[3]
level_win = datas[2]

current_music = -1
score = datas[0]
numero_joueur = datas[1]
mouse_scroll_niveaux = 0

MAIN = 0
LEVELS = 1
MINIGAMES = 2
CREATED_LVLS = 3
CREATE = 4
PAUSE = 5
SKINS = 6
GAME = 7
menu = MAIN
last_menu = MAIN


lock_lines = True
lock_game_over = False
mode_dev = False
random_mg = False

classement = [
    "TRAZE:  01:53:12",
    "DOAN:  03:00:00",
    "BOTSWANA: 04:00:00",
    "WAREX: 04:57:98",
    "TITOUAN56:  05:00:00"
]

mondes = [
    [1,2,3,4,5],
    [7,8,9,10,11,12,13],
    [15,16,17,18],
    [6,14,19],
    [20],
    [101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116],
    [1,2,3,4,3,4]
]

type_minigame = [
    [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,20], #normal
    [10,19], #gliding
    [101,105], #flappy_bird
    [], #double_jump
    [102,108], #speed
    [103,107], #ice
    [104,106], #big_jump
    [109,116], #inversed_controls
    [110,113], #small
    [111], #big
    [112], #crossy_road
    [114], #kangourou
    [115], #snowy_snow
    ["normal", "gliding", "flappy_bird", "double_jump", "speed", "ice", "big_jump", "inversed_controls", "small", "big", "crossy_road", "kangourou", "snowy_snow"]
]

difficulte = ["Facile", "Moyen", "Difficile", "Bonus", "Impossible", "Mini-jeu!"]
minigame_type = ["flappy_bird", "x2_speed", "glace", "big_jump", "flappy_bird", "big_jump", "glace", "x2_speed", "inversed_controls", "small", "big", "crossy_road", "small", "kangourou", "snowy_snow", "inversed_controls"]
number_minigame = ["1","1","1","1","2","2","2","2","1","1","1","1","2","1","1","2"]
minigame_name = ["Flappy Oiseau", "Subway Coureur", "Attention glissade", "Moon Boots", "Flappy Oiseau le retour", "To the Moon, again", "Pingouin", "Subway Coureur 2", "Comme un léger problème...", "C'est pas la taille qui compte!", "King Kong joined the game", "Traversage de route", "Petit mais costaud", "Sboing Sboing", "Arithmétique Dash", "Contresens"]
skin_prices = datas[4]
skin_ordre = [1,2,6,7,5,11,4,8,10,3,9]
texte = ""
level_names = datas[5]

#load de trucs--------------------------------------------------------------------------------------


def change_music(current_music, numero_music):
    if not current_music == numero_music:
        if path.exists(f"sounds/background_msc_{numero_music}.mp3"):
            pygame.mixer.music.load(f"sounds/background_msc_{numero_music}.mp3")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1, 0.0, 5000)
        else:
            pygame.mixer.music.unload()

def reset_level(level, groups):
    player.reset(100, SCREEN_HEIGHT - 150)
    for group in groups:
        group.empty()
    world_data = []
    if path.exists(f"levels/level{level}_data"):
        pickle_read = open(f"levels/level{level}_data", "rb")
        world_data = pickle.load(pickle_read)
        world = World(world_data)
    return world

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
        draw_text(message, font1, clr_white, (SCREEN_WIDTH - text_width) // 2, (SCREEN_HEIGHT - text_height) // 2 - 100)
        draw_text("press Enter to finish", font3, color, SCREEN_WIDTH - 300, SCREEN_HEIGHT - 50)
        text_width, text_height = font2.size(text)
        draw_text(text, font2, clr_white, (SCREEN_WIDTH - text_width) // 2, (SCREEN_HEIGHT - text_height) // 2)
        pygame.display.flip()
        CLOCK.tick(30)
    return text

def waiting_screen(waiting_screen, text1, text2, font, time, screen):
    screen.blit(waiting_screen, (0,0))
    text_width, text_height = font.size(f"{text1}")
    draw_text(f"{text1}", font, clr_white, (SCREEN_WIDTH - text_width) // 2, (SCREEN_HEIGHT - text_height) // 2)
    text_width, text_height = font.size(f"{text2}")
    draw_text(f"{text2}", font, clr_white, (SCREEN_WIDTH - text_width) // 2, (SCREEN_HEIGHT - text_height) // 2 + 100)
    pygame.display.flip()
    pygame.time.delay(time * 15)

def save():
    pickle_out = open('data/data_main', 'wb')
    datas[0] = score
    datas[1] = numero_joueur
    datas[2] = level_win
    datas[3] = nb_created_levels
    datas[4] = skin_prices
    datas[5] = level_names
    pickle.dump(datas, pickle_out)
    pickle_out.close()
    pygame.time.delay(180)

def mouse_scrolling(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:  # Scrolling up
            return 50
        elif event.button == 5:  # Scrolling down
            return -50
        else:
            return 0
    else:
        return 0



#images---------------------------------------------------------------------------
img_bouton_restart = pygame.image.load("sprites/img_bouton_restart.webp")
img_bouton_exit = pygame.image.load("sprites/img_bouton_exit.webp")
img_bouton_back = pygame.image.load("sprites/img_bouton_back.webp")
img_bouton_menu = pygame.image.load("sprites/img_bouton_menu.webp")
img_bouton_menu_pause = pygame.image.load("sprites/img_bouton_menu_pause.webp")
img_bouton_resume_pause = pygame.image.load("sprites/img_bouton_resume_pause.webp")
img_bouton_start = pygame.image.load("sprites/img_bouton_start.webp")
img_bouton_niveaux = pygame.image.load("sprites/img_bouton_niveaux.webp")
img_cadenas = pygame.image.load("sprites/img_cadenas.webp")
img_bouton_random_mg = pygame.image.load("sprites/img_bouton_random_mg.webp")
img_bouton_create = pygame.image.load("sprites/img_bouton_create.webp")
img_bouton_skins = pygame.image.load("sprites/img_bouton_skins.webp")
img_bouton_add = pygame.image.load("sprites/img_bouton_add.webp")
img_bouton_delete = pygame.image.load("sprites/img_bouton_delete.webp")
#----------------------
img_background_menu = pygame.image.load("sprites/img_background_menu.webp")
img_background_menu = pygame.transform.scale(img_background_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
img_background_score = pygame.image.load("sprites/img_background_score.webp")
img_background_mort = pygame.image.load("sprites/img_background_mort.webp")
img_background_pause = pygame.image.load("sprites/img_background_pause.webp")
img_background_joueur_1 = pygame.image.load("sprites/img_background_joueur_1.webp")
img_background_joueur_1 = pygame.transform.scale(img_background_joueur_1, (400, 550))
img_background_joueur_2 = pygame.image.load("sprites/img_background_joueur_2.webp")
img_background_joueur_2 = pygame.transform.scale(img_background_joueur_1, (400, 550))
#--------------------
img_waiting_screen_1 = pygame.image.load(f"sprites/img_background_waiting_screen_1.webp")
img_waiting_screen_1 = pygame.transform.scale(img_waiting_screen_1, (SCREEN_WIDTH, SCREEN_HEIGHT))
#--------------------
img_fleche = pygame.image.load("sprites/img_fleche.webp")
img_fleche_flip = pygame.transform.flip(img_fleche, True, False)
img_coin_score = pygame.image.load("sprites/img_coin_score.webp")
img_coin_price = pygame.image.load("sprites/img_coin.webp")
img_joueur_select = pygame.image.load("sprites/img_joueur_select.webp")
#sons------------------------------------------------------------------------------
jump_msc = pygame.mixer.Sound("sounds/jump_msc.wav")
jump_msc.set_volume(0.7)
coin_msc = pygame.mixer.Sound("sounds/coin_msc.mp3")
coin_msc.set_volume(1)
game_over_msc = pygame.mixer.Sound("sounds/game_over_msc.mp3")
game_over_msc.set_volume(1)


#world -------------------------------------------------------------------------------------------------------


class World():
    def __init__(self, data):
        self.tile_list = []

        row_count = 0 - OFFSET
        for row in data:
            col_count = -1
            for tile in row:

                if tile == 1378:
                    background = Fond(monde)
                    fond_group.add(background)
                if tile == 1:
                    dirt = Bloc(col_count * TILE_SIZE, row_count * TILE_SIZE, "dirt", monde)
                    bloc_group.add(dirt)
                if tile == 2:
                    grass = Bloc(col_count * TILE_SIZE, row_count * TILE_SIZE, "grass", monde)
                    bloc_group.add(grass)
                if tile == 3:
                    ennemi1a = Ennemi1a(col_count * TILE_SIZE, row_count * TILE_SIZE + 10)
                    ennemi_group.add(ennemi1a)
                if tile == 4:
                    pics = Pics(col_count * TILE_SIZE, row_count * TILE_SIZE + 20, "down")
                    pics_group.add(pics)
                if tile == 5:
                    stone = Bloc(col_count * TILE_SIZE, row_count * TILE_SIZE, "stone", monde)
                    bloc_group.add(stone)
                if tile == 6:
                    lave = Lave(col_count * TILE_SIZE, row_count * TILE_SIZE + 20, "lave")
                    lave_group.add(lave)
                if tile == 7:
                    lava_full = Lave(col_count * TILE_SIZE, row_count * TILE_SIZE, "lave_full")
                    lave_group.add(lava_full)
                if tile == 8:
                    porte = Exit(col_count * TILE_SIZE, row_count * TILE_SIZE + 20)
                    exit_group.add(porte)
                if tile == 9:
                    coin = Coin(col_count * TILE_SIZE + (TILE_SIZE // 2), row_count * TILE_SIZE + (TILE_SIZE // 2), "normal")
                    coin_group.add(coin)
                if tile == 10:
                    plateforme_x = Plateforme(col_count * TILE_SIZE, row_count * TILE_SIZE + 25, 1, 0)
                    plateforme_group.add(plateforme_x)	
                if tile == 11:
                    plateforme_y = Plateforme(col_count * TILE_SIZE, row_count * TILE_SIZE + 25, 0, 1)
                    plateforme_group.add(plateforme_y)
                if tile == 12:
                    ennemi2a = Ennemi2a(col_count * TILE_SIZE, row_count * TILE_SIZE)		
                    ennemi_group.add(ennemi2a)	
                if tile == 13:
                    ennemi2b = Ennemi2b(col_count * TILE_SIZE, row_count * TILE_SIZE)		
                    ennemi_group.add(ennemi2b)	
                if tile == 14:
                    ennemi1b = Ennemi1b(col_count * TILE_SIZE, row_count * TILE_SIZE + 10)
                    ennemi_group.add(ennemi1b)
                if tile == 15:
                    bumper = Bumper(col_count * TILE_SIZE, row_count * TILE_SIZE + 20)
                    bumper_group.add(bumper)
                if tile == 16:
                    ennemi3a = Ennemi3a(col_count * TILE_SIZE, row_count * TILE_SIZE - 10)
                    ennemi_group.add(ennemi3a)
                if tile == 17:
                    plateforme = Plateforme(col_count * TILE_SIZE, row_count * TILE_SIZE + 25, 2, 0)
                    plateforme_group.add(plateforme)	
                if tile == 18:
                    plateforme = Plateforme(col_count * TILE_SIZE, row_count * TILE_SIZE + 25, 0, 2)
                    plateforme_group.add(plateforme)				
                if tile == 19:
                    firemaker = Firemaker(col_count * TILE_SIZE, row_count * TILE_SIZE - 50)
                    firemaker_group.add(firemaker)
                if tile == 20:
                    flower = Decoration(col_count * TILE_SIZE + 20, row_count * TILE_SIZE + 25, "flower", monde)
                    decoration_group.add(flower)
                if tile == 21:
                    bloc_break = Bloc_breakable(col_count * TILE_SIZE, row_count * TILE_SIZE, "platform")
                    bloc_group.add(bloc_break)
                if tile == 22:
                    tronc = Bloc(col_count * TILE_SIZE, row_count * TILE_SIZE + 20, "tronc", monde)
                    bloc_group.add(tronc)
                if tile == 23:
                    panneau = Decoration(col_count * TILE_SIZE, row_count * TILE_SIZE, "panneau", monde)
                    decoration2_group.add(panneau)
                if tile == 24:
                    champi = Decoration(col_count * TILE_SIZE + 10, row_count * TILE_SIZE + 30, "champi", monde)
                    decoration_group.add(champi)
                if tile == 25:
                    herbe = Decoration(col_count * TILE_SIZE + 10, row_count * TILE_SIZE + 30, "herbe", monde)
                    decoration2_group.add(herbe)
                if tile == 26:
                    hautes_herbes = Decoration(col_count * TILE_SIZE, row_count * TILE_SIZE - 50, "hautes_herbes", monde)
                    decoration2_group.add(hautes_herbes)
                if tile == 27:
                    big_coin = Coin(col_count * TILE_SIZE, row_count * TILE_SIZE + 25, "big")
                    coin_group.add(big_coin)
                    big_coin_group.add(big_coin)
                if tile == 28:
                    hautes_herbes2 = Decoration(col_count * TILE_SIZE, row_count * TILE_SIZE + 15, "buisson", monde)
                    decoration2_group.add(hautes_herbes2)
                if tile == 29:
                    pics_up = Pics(col_count * TILE_SIZE, row_count * TILE_SIZE, "up")
                    pics_group.add(pics_up)
                if tile == 30:
                    deathwall = Deathwall(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    ennemi_group.add(deathwall)
                if tile == 31:
                    ennemi4a = Ennemi4a(col_count * TILE_SIZE, row_count * TILE_SIZE, 2, 4)		
                    ennemi_group.add(ennemi4a)	
                if tile == 32:
                    ennemi5a = Ennemi5a(col_count * TILE_SIZE, row_count * TILE_SIZE)		
                    ennemi_group.add(ennemi5a)
                if tile == 33:
                    fake_grass = Decoration(col_count * TILE_SIZE, row_count * TILE_SIZE, "fake_grass", monde)
                    decoration2_group.add(fake_grass)


                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            SCREEN.blit(tile[0], tile[1])

if path.exists(f"levels/level{level}_data"):
    pickle_read = open(f"levels/level{level}_data", "rb")
    world_data = pickle.load(pickle_read)
    world = World(world_data)










#DEF DU JOUEUR -------------------------------------------------------------------------------------------------------------------------------------------------------------










class Joueur():
    def __init__(self, x, y, numero_joueur):
        self.img = pygame.image.load(f"sprites/img_joueur_{numero_joueur}_0.webp")
        self.reset(x, y)

    def update(self, game_over):
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
                    if player.airtime == False and player.rect.y > platform.rect.y:
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
                            player.rect.x += platform.move_x * platform.direction
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
        SCREEN.blit(self.image, self.rect)

        return game_over
    
    
    def reset(self, x, y):

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

player = Joueur(95, SCREEN_HEIGHT - 140, numero_joueur)



#LANCEMENT DU JEU -----------------------------------------------------------------------------------------------------------------------------------------------



#LES BOUTONSSSSSSS (une vraie galère)
bouton_exit = Bouton(SCREEN_WIDTH - 105, 15, 90, 50, img_bouton_exit)
bouton_restart = Bouton(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 45, 250, 100, img_bouton_restart)
bouton_menu = Bouton(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 95, 250, 100, img_bouton_menu)
bouton_back = Bouton(15, 15, SCREEN_WIDTH // 9, SCREEN_HEIGHT // 14, img_bouton_back)
bouton_resume_pause = Bouton(SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2 - 40, 312, 142, img_bouton_resume_pause)
bouton_menu_pause = Bouton(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 40, 312, 142, img_bouton_menu_pause)
bouton_start = Bouton(SCREEN_WIDTH // 2 + 95, SCREEN_HEIGHT // 2 - 45, 260, 100, img_bouton_start)
bouton_niveaux = Bouton(SCREEN_WIDTH // 2 + 75, SCREEN_HEIGHT // 2 + 85, 300, 100, img_bouton_niveaux)
bouton_create = Bouton(SCREEN_WIDTH // 2 + 85, SCREEN_HEIGHT // 2 + 215, 280, 100, img_bouton_create)
bouton_skins = Bouton(SCREEN_WIDTH // 2 - 363, SCREEN_HEIGHT // 2 + 250, 226, 100, img_bouton_skins)
bouton_suite = Bouton(SCREEN_WIDTH - (SCREEN_WIDTH // 20 + 35), SCREEN_HEIGHT // 2 , SCREEN_WIDTH // 20, SCREEN_HEIGHT // 9, img_fleche)
bouton_retour = Bouton(35, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 20, SCREEN_HEIGHT // 9, img_fleche_flip)
bouton_random_mg = Bouton(SCREEN_WIDTH // 2 - 235, SCREEN_HEIGHT // 2 - 150, 250, 50, img_bouton_random_mg)
bouton_add = Bouton(SCREEN_WIDTH // 2 - 185, SCREEN_HEIGHT // 2 - 200, 100, 100, img_bouton_add)
bouton_delete = Bouton(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 185, 70, 70, img_bouton_delete)


boutons_menu = [bouton_exit, bouton_niveaux, bouton_start, bouton_create, bouton_skins]


run=True
while run==True:

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            save()
            run = False

    CLOCK.tick(FPS)
    key = pygame.key.get_pressed()



    if menu == MAIN:
        change_music(current_music, 0)
        current_music = 0
        SCREEN.blit(img_background_menu, (0,0))
        SCREEN.blit(img_background_joueur_1, (SCREEN_WIDTH // 2 - 457, SCREEN_HEIGHT // 2 - 175))
        SCREEN.blit(img_background_joueur_2, (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - 175))
        draw_text('Choix du perso', font_lilitaone_50, clr_black, SCREEN_WIDTH // 2 - 415, SCREEN_HEIGHT // 2 - 160, SCREEN)
        draw_text('Naviguation', font_lilitaone_50, clr_black, SCREEN_WIDTH // 2 + 90, SCREEN_HEIGHT // 2 - 130, SCREEN)
        draw_text(f'Vous avez {score} pièces', font_bauhaus_40, clr_black, 10, 10, SCREEN)

        handable = 0
        for bouton in boutons_menu:
            if bouton.rect.collidepoint(pygame.mouse.get_pos()):
                handable += 1
        if not handable == 0:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        SCREEN.blit(img_joueur_select, (SCREEN_WIDTH // 2 - 345, SCREEN_HEIGHT // 2 - 90))
        SCREEN.blit(pygame.image.load(f"sprites/img_joueur_{numero_joueur}_menu.webp"), (SCREEN_WIDTH // 2 - 330, SCREEN_HEIGHT // 2 - 75))
        #draw_text(f"{nom_joueur[numero_joueur - 1]}", font_lilitaone_50, clr_black, screen_width // 2 - 220, screen_height // 2 + 20)

        if bouton_exit.draw(1, SCREEN) or key[pygame.K_e]:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            save()
            run = False
        if bouton_niveaux.draw(1, SCREEN) or key[pygame.K_n]:
            pygame.time.delay(45)
            menu = LEVELS
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if bouton_skins.draw(1, SCREEN) or key[pygame.K_k]:
            pygame.time.delay(45)
            menu = SKINS
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if bouton_create.draw(1, SCREEN) or key[pygame.K_c]:
            pygame.time.delay(45)
            menu = CREATE
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if bouton_start.draw(1, SCREEN) or key[pygame.K_s]:
            pygame.time.delay(15)
            menu = GAME
            level = 0
            game_over = 1
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            
            
    elif menu == LEVELS:

        change_music(current_music, 0)
        current_music = 0
        SCREEN.blit(img_background_menu, (0,0))
        draw_text('Levels:', font_lilitaone_60, clr_black, 140, SCREEN_HEIGHT // 2 - 200 + mouse_scroll_niveaux)

        if key[pygame.K_t]:
            level_win = nb_levels_main_quest
            mode_dev = True
            score = 99999
        if mode_dev:
            draw_text('Dev mode', font_ubuntu_30, clr_black, SCREEN_WIDTH * 5 // 8, SCREEN_HEIGHT * 7 // 8 + mouse_scroll_niveaux)

        for event in pygame.event.get():
            mouse_scroll_niveaux += mouse_scrolling(event)
            if mouse_scroll_niveaux >= 0:
                mouse_scroll_niveaux = 0
            if mouse_scroll_niveaux <= -200:
                mouse_scroll_niveaux = -200

        for i in range(level_win):

            for k in range(len(mondes) - 1):
                if i+1 in mondes[k]:
                    level_num = k+1

            i2 = i
            j = i // 8
            i = i % 8

            bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4), SCREEN_HEIGHT // 2 - 50 + 140 * j + mouse_scroll_niveaux, 100, 100, pygame.image.load(f"sprites/img_bouton_niveau_on_{level_num}_petit.webp"))
            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4) - 5, SCREEN_HEIGHT // 2 - 55 + 140 * j + mouse_scroll_niveaux, 110, 110, pygame.image.load(f"sprites/img_bouton_niveau_on_{level_num}_gros.webp"))

            if bouton_niveau.draw(2, SCREEN):
                pygame.time.delay(30)
                menu = GAME
                last_menu = LEVELS
                level = i2 
                game_over = 1

            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                text_width, text_height = font_lilitaone_80.size(str(i2 + 1))
                if i2 + 1 in mondes[4]:
                    draw_text(f"{i2 + 1}", font_lilitaone_80, clr_white, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j + mouse_scroll_niveaux)
                else:
                    draw_text(f"{i2 + 1}", font_lilitaone_80, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j + mouse_scroll_niveaux)
            else:
                text_width, text_height = font_lilitaone_70.size(str(i2 + 1))
                if i2 + 1 in mondes[4]:
                    draw_text(f"{i2 + 1}", font_lilitaone_70, clr_white, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j + mouse_scroll_niveaux)
                else:
                    draw_text(f"{i2 + 1}", font_lilitaone_70, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j + mouse_scroll_niveaux)

        for i in range(level_win, nb_levels_main_quest):

            for k in range(len(mondes) - 1):
                if i + 1 in mondes[k]:
                    level_num = k + 1

            i2 = i
            j2 = i // 8
            i = i % 8

            SCREEN.blit(pygame.image.load(f"sprites/img_bouton_niveau_off_{level_num}.webp"), (SCREEN_WIDTH // 2 + 140 * (i - 4), SCREEN_HEIGHT // 2 - 50 + 140 * j2 + mouse_scroll_niveaux))
            text_width, text_height = font_lilitaone_70.size(str(i2 + 1))
            if i2 + 1 in mondes[4]:
                draw_text(f"{i2 + 1}", font_lilitaone_70, clr_white_minus, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j2 + mouse_scroll_niveaux)
            else:
                draw_text(f"{i2 + 1}", font_lilitaone_70, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j2 + mouse_scroll_niveaux)
            SCREEN.blit(img_cadenas, (SCREEN_WIDTH // 2 + 140 * (i - 4) + 6, SCREEN_HEIGHT // 2 - 45 + 140 * j2 + mouse_scroll_niveaux))

        if bouton_back.draw(1, SCREEN) or key[pygame.K_ESCAPE]:
            pygame.time.delay(20)
            menu = LEVELS
        
        if bouton_suite.draw(1, SCREEN):
            pygame.time.delay(30)
            menu = MINIGAMES
        
        if bouton_delete.draw(1, SCREEN):
            level_win = 1




    elif menu == MINIGAMES:


        change_music(current_music, 0)
        current_music = 0
        SCREEN.blit(img_background_menu, (0,0))
        draw_text('Mini-jeux:', font_lilitaone_60, clr_black, 140, SCREEN_HEIGHT // 2 - 200)
        draw_text("more soon...", font_bauhaus_50, clr_black, SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT * 5 // 6)

        if bouton_retour.draw(1, SCREEN):
            pygame.time.delay(30)
            menu = LEVELS

        if bouton_suite.draw(1, SCREEN):
            pygame.time.delay(30)
            menu = CREATED_LVLS

        if bouton_back.draw(1, SCREEN) or key[pygame.K_ESCAPE]:
            pygame.time.delay(20)
            menu = MINIGAMES
        
        if bouton_random_mg.draw(1, SCREEN):    
            random_mg = True
            pygame.time.delay(30)
            menu = GAME
            last_menu = MINIGAMES
            level = 101
            game_over = 1  
        draw_text("RANDOM", font_bauhaus_40, clr_black, SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 146)          


        for i in range(nb_minis_jeux):
            level_num = 6

            i2 = i
            j = i // 8
            i = i % 8

            bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4), SCREEN_HEIGHT // 2 - 50 + 140 * j, 100, 100, pygame.image.load(f"sprites/img_bouton_niveau_on_{level_num}_petit.webp"))
            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4) - 5, SCREEN_HEIGHT // 2 - 55 + 140 * j, 110, 110, pygame.image.load(f"sprites/img_bouton_niveau_on_{level_num}_gros.webp"))

            if bouton_niveau.draw(2, SCREEN):
                pygame.time.delay(30)
                menu = GAME
                last_menu = MINIGAMES
                level = 100 + i2
                game_over = 1

            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                SCREEN.blit(pygame.image.load(f"sprites/img_{minigame_type[i2]}.webp"), (SCREEN_WIDTH // 2 + 140 * (i - 4) + 5, SCREEN_HEIGHT // 2 - 45 + 140 * j))
                if not number_minigame[i2] == "1":
                    draw_text(number_minigame[i2], font_lilitaone_30, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 76, SCREEN_HEIGHT // 2 - 50 + 140 * j)
            else:
                SCREEN.blit(pygame.image.load(f"sprites/img_{minigame_type[i2]}_petit.webp"), (SCREEN_WIDTH // 2 + 140 * (i - 4) + 5, SCREEN_HEIGHT // 2 - 45 + 140 * j))
                if not number_minigame[i2] == "1":
                    draw_text(number_minigame[i2], font_lilitaone_30, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 72, SCREEN_HEIGHT // 2 - 45 + 140 * j)
        



    elif menu == CREATED_LVLS:

        change_music(current_music, 0)
        current_music = 0
        SCREEN.blit(img_background_menu, (0,0))
        draw_text('Niveaux créés:', font_lilitaone_60, clr_black, 140, SCREEN_HEIGHT // 2 - 200)

        if key[pygame.K_t]:
            level_win = nb_levels_main_quest
            mode_dev = True
        if mode_dev:
            draw_text('mode développeur activé', font_ubuntu_30, clr_black, SCREEN_WIDTH * 5 // 8, SCREEN_HEIGHT * 7 // 8)

        for i in range(nb_created_levels):

            for k in range(len(mondes) - 1):
                if i + 1 in mondes[k]:
                    level_num = k + 1

            i2 = i
            j = i // 8
            i = i % 8

            bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4), SCREEN_HEIGHT // 2 - 50 + 140 * j, 100, 100, pygame.image.load(f"sprites/img_bouton_niveau_on_1_petit.webp"))
            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4) - 5, SCREEN_HEIGHT // 2 - 55 + 140 * j, 110, 110, pygame.image.load(f"sprites/img_bouton_niveau_on_1_gros.webp"))

            if bouton_niveau.draw(2, SCREEN):
                pygame.time.delay(30)
                menu = GAME
                last_menu = CREATED_LVLS
                level = 200 + i2
                game_over = 1

            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                text_width, text_height = font_lilitaone_80.size(str(i2 + 1))
                draw_text(f"{i2 + 1}", font_lilitaone_80, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j)
            else:
                text_width, text_height = font_lilitaone_70.size(str(i2 + 1))
                draw_text(f"{i2 + 1}", font_lilitaone_70, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j)

        if bouton_back.draw(1, SCREEN) or key[pygame.K_ESCAPE]:
            pygame.time.delay(20)
            menu = MAIN
        
        if bouton_retour.draw(1, SCREEN):
            pygame.time.delay(30)
            menu = MINIGAMES




    elif menu == CREATE:

        change_music(current_music, 0)
        current_music = 0
        SCREEN.blit(img_background_menu, (0,0))
        draw_text('Vos niveaux:', font_lilitaone_60, clr_black, 140, SCREEN_HEIGHT // 2 - 200)

        for i in range(nb_created_levels):

            for k in range(len(mondes) - 1):
                if i + 1 in mondes[k]:
                    level_num = k + 1

            i2 = i
            j = i // 8
            i = i % 8

            bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4), SCREEN_HEIGHT // 2 - 50 + 140 * j, 100, 100, pygame.image.load(f"sprites/img_bouton_niveau_on_1_petit.webp"))
            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4) - 5, SCREEN_HEIGHT // 2 - 55 + 140 * j, 110, 110, pygame.image.load(f"sprites/img_bouton_niveau_on_1_gros.webp"))


            if bouton_niveau.draw(2, SCREEN):
                img_background_waiting_screen = pygame.image.load(f"sprites/img_background_waiting_screen_3.webp")
                img_background_waiting_screen = pygame.transform.scale(img_background_waiting_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
                waiting_screen(img_background_waiting_screen, "Création de niveaux", f"Niveau {i2 + 1}", font_lilitaone_80, 60, SCREEN)
                level_names[i2+1] = write(level_names[i2+1], font_lilitaone_80, font_bauhaus_50, font_ubuntu_30, clr_white, "Entrez un nom pour le niveau:", 20)
                main(201 + i2)

            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                text_width, text_height = font_lilitaone_80.size(str(i2 + 1))
                draw_text(f"{i2 + 1}", font_lilitaone_80, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j)
            else:
                text_width, text_height = font_lilitaone_70.size(str(i2 + 1))
                draw_text(f"{i2 + 1}", font_lilitaone_70, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j)


        if bouton_add.draw(1, SCREEN) and nb_created_levels < 20:
            nb_created_levels += 1

        if bouton_delete.draw(1, SCREEN) and nb_created_levels > 1:
            nb_created_levels -= 1


        if bouton_back.draw(1, SCREEN) or key[pygame.K_ESCAPE]:
            pygame.time.delay(20)
            menu = MAIN




    elif menu == SKINS:

        change_music(current_music, 0)
        current_music = 0
        SCREEN.blit(img_background_menu, (0,0))
        draw_text('Galerie des skins:', font_lilitaone_60, clr_black, 140, SCREEN_HEIGHT // 2 - 200)
        draw_text(f'Vous avez {score} pièces', font_lilitaone_70, clr_black, SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 150)

        for i in range(nb_skins):

            for k in range(len(mondes) - 1):
                if i + 1 in mondes[k]:
                    level_num = k + 1

            i2 = i
            j = i // 8
            i = i % 8

            if numero_joueur != skin_ordre[i2]:
                bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4), SCREEN_HEIGHT // 2 - 50 + 140 * j, 100, 100, pygame.image.load("sprites/img_bouton_niveau_on_1_petit.webp"))
                if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                    bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4) - 5, SCREEN_HEIGHT // 2 - 55 + 140 * j, 110, 110, pygame.image.load("sprites/img_bouton_niveau_on_1_gros.webp"))

            else:
                bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4), SCREEN_HEIGHT // 2 - 50 + 140 * j, 100, 100, pygame.image.load("sprites/img_bouton_niveau_on_3_petit.webp"))
                if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                    bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4) - 5, SCREEN_HEIGHT // 2 - 55 + 140 * j, 110, 110, pygame.image.load("sprites/img_bouton_niveau_on_3_gros.webp"))

            if bouton_niveau.draw(2, SCREEN):
                if not skin_prices[i2] == 0: 
                    if score >= skin_prices[i2]:
                        score -= skin_prices[i2]
                        skin_prices[i2] = 0
                else:
                    numero_joueur = skin_ordre[i2]

            SCREEN.blit(pygame.image.load(f"sprites/img_joueur_{skin_ordre[i2]}_icon.webp"), (SCREEN_WIDTH // 2 + 140 * (i - 4), SCREEN_HEIGHT // 2 - 53 + 140 * j))
            if not skin_prices[i2] == 0:
                SCREEN.blit(img_cadenas, (SCREEN_WIDTH // 2 + 140 * (i - 4) + 6, SCREEN_HEIGHT // 2 - 45 + 140 * j))
                draw_text(f"{skin_prices[i2]}", font_lilitaone_30, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 12, SCREEN_HEIGHT // 2 + 10 + 140 * j)
                SCREEN.blit(img_coin_price, (SCREEN_WIDTH // 2 + 140 * (i - 4) + 64, SCREEN_HEIGHT // 2 + 15 + 140 * j))


            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                SCREEN.blit(pygame.image.load("sprites/img_bouton_niveau_0_gros.webp"), (SCREEN_WIDTH // 2 + 140 * (i - 4) - 5, SCREEN_HEIGHT // 2 - 55 + 140 * j))
            else:
                SCREEN.blit(pygame.image.load("sprites/img_bouton_niveau_0.webp"), (SCREEN_WIDTH // 2 + 140 * (i - 4), SCREEN_HEIGHT // 2 - 50 + 140 * j))
            

        if bouton_back.draw(1, SCREEN) or key[pygame.K_ESCAPE]:
            pygame.time.delay(20)
            menu = MAIN

        if key[pygame.K_t]:
            level_win = nb_levels_main_quest
            mode_dev = True
            score = 99999 




    else:

        world.draw()

        change_music(current_music, monde)
        current_music = monde

        if game_over == 0:
            if lock_lines == True:
                lock_lines = False
                lock_game_over = False
            #drawwwwww un max
            full_draw(groups)
            game_over = player.update(game_over)
            decoration2_group.draw(SCREEN)
            #update default = mouvement + animation 
            full_update(groups)

            if key[pygame.K_ESCAPE]:
                menu = PAUSE
            
            if pygame.sprite.spritecollide(player, big_coin_group, True):
                coin_msc.play()
                score += 10
            if pygame.sprite.spritecollide(player, coin_group, True):
                coin_msc.play()
                score += 1
            SCREEN.blit(img_background_score, (50,50))
            SCREEN.blit(img_coin_score, (357,85))
            draw_text('x ' + str(score), font_bauhaus_50, clr_black, TILE_SIZE + 350, 70)
            draw_text('niveau: ' + str(level), font_bauhaus_50, clr_black, TILE_SIZE + 40, 70)


            if type_level == "crossy_road":

                if player.rect.x > SCREEN_WIDTH // 2 + 100:
                    SCREEN_SCROLL = -50
                    player.rect.x -= 50
                    #update scroll = bah quand l'écran défile les objets bougent
                    full_scroll(groups)
                    
                elif player.rect.x < 400 and player.mostleftposition > 305:
                    SCREEN_SCROLL = 50
                    player.rect.x += 50
                    full_scroll(groups)

                else:
                    SCREEN_SCROLL = 0

            else:

                if player.rect.x > SCREEN_WIDTH // 2 + 100:
                    SCREEN_SCROLL = -1 * player.vitesse_x
                    player.rect.x -= player.vitesse_x
                    #update scroll = bah quand l'écran défile les objets bougent
                    full_scroll(groups)
                    
                elif player.rect.x < 400 and player.mostleftposition > 305:
                    SCREEN_SCROLL = -1 * player.vitesse_x
                    player.rect.x -= player.vitesse_x
                    full_scroll(groups)

                else:
                    SCREEN_SCROLL = 0

            #background_msc.play()



        if game_over == -1:
            if not lock_game_over:
                game_over_msc.play()
                lock_game_over = True
            fond_group.draw(SCREEN)
            game_over = player.update(game_over)
            full_draw(groups)
            SCREEN.blit(img_background_score, (50,50))
            SCREEN.blit(img_coin_score, (357,85))
            draw_text('x ' + str(score), font_bauhaus_50, clr_black, TILE_SIZE + 350, 70)
            draw_text('niveau: ' + str(level), font_bauhaus_50, clr_black, TILE_SIZE + 40, 70)
            SCREEN.blit(img_background_mort, (SCREEN_WIDTH // 2 - 200,SCREEN_HEIGHT // 2 - 200))
            lines = ["pfff really?","how u so bad?","skill issue?","not even close","nice death"]
            if lock_lines == False:
                random_line = random.randint(0, len(lines) - 1)
                lock_lines = True
            text_width, text_height = font_lilitaone_60.size(lines[random_line])
            draw_text(lines[random_line], font_lilitaone_60, clr_brown, SCREEN_WIDTH // 2 - text_width // 2, SCREEN_HEIGHT // 2 - 150)
            draw_text("press enter to restart", font_ubuntu_30, clr_brown, SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 2 + 235)
            if bouton_restart.rect.collidepoint(pygame.mouse.get_pos()) or bouton_menu.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if bouton_restart.draw(1, SCREEN) or key[pygame.K_RETURN]:
                pygame.time.delay(30)
                player.mostleftposition = 0
                world_data = []
                world = reset_level(level, groups)
                game_over = 0
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if bouton_menu.draw(1, SCREEN):
                pygame.time.delay(45)
                menu = last_menu
                game_over = 0
                level = 1
                monde = 1
                random_mg = False
                world = reset_level(1, groups)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)



        if menu == PAUSE:

            SCREEN.blit(img_background_pause, (SCREEN_WIDTH // 2 - 500, SCREEN_HEIGHT // 2 - 250))
            game_over = 2
            if bouton_resume_pause.rect.collidepoint(pygame.mouse.get_pos()) or bouton_menu_pause.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if bouton_resume_pause.draw(1, SCREEN):
                pygame.time.delay(30)
                game_over = 0
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if bouton_menu_pause.draw(1, SCREEN):
                pygame.time.delay(45)
                game_over = 0
                level = 1
                monde = 1
                random_mg = False
                player.reset(100, SCREEN_HEIGHT - 150)
                reset_level(level, groups)
                menu = last_menu
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


        if game_over == 1:
            
            if level % 100 < nb_levels:
                if level // 100 == 0 or level // 100 == 2:
                    level+=1
                elif level // 100 == 1:
                    if not random_mg:
                        level+=1
                    else:
                        level = 100 + random.randint(1,nb_minis_jeux)

                if level_win < level + 1 < nb_levels_main_quest:
                    level_win = level

                for i in range(len(mondes) - 1):
                    if level in mondes[i]:
                        monde = mondes[len(mondes) - 1][i]

                for i in range(len(type_minigame) - 1):
                    if level in type_minigame[i]:
                        type_level = type_minigame[len(type_minigame) - 1][i]


                if level in mondes[4]:
                    monde = 5
                if level in mondes[5]:
                    monde = 6
                img_waiting_screen = pygame.image.load(f"sprites/img_background_waiting_screen_{monde}.webp")
                img_background_waiting_screen = pygame.image.load(f"sprites/img_background_waiting_screen_{monde}.webp")
                img_background_waiting_screen = pygame.transform.scale(img_background_waiting_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
                SCREEN.blit(img_background_waiting_screen, (0,0))
                if level // 100 == 0:
                    waiting_screen(img_waiting_screen, f"Niveau {level}", difficulte[monde - 1], font_lilitaone_80, 80, SCREEN)
                if level // 100 == 1:
                    waiting_screen(img_waiting_screen, f"Mini-jeu {level - 100}", minigame_name[level - 101], font_lilitaone_80, 80, SCREEN)                 
                if level // 100 == 2:   
                    waiting_screen(img_waiting_screen, f"Niveau créé n°{level - 200}", level_names[level - 200], font_lilitaone_80, 100, SCREEN)
                if level in mondes[4]:
                    monde = 3
                if level in mondes[5]:
                    monde = 4

                game_over = 0
                world = reset_level(level, groups)

            else:
                msg=["MINH", "DOAN"]
                draw_text(f'TU AS TROUVE {msg[numero_joueur - 1]}!', font_lilitaone_60, clr_blue, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 170)
                if bouton_restart.draw(1, SCREEN) or key[pygame.K_RETURN] == True:
                    menu = last_menu
                    player.direction = 1
                    level = 1
                    monde = 1
                    world = reset_level(level, groups)
                    game_over = 0

        #draw_grid()

    pygame.display.update()


pygame.quit()