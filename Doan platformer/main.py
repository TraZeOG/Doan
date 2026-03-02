from imports import *
from assets import *
from world import *
from player import *

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
            pygame.mixer.music.set_volume(0.05)
            pygame.mixer.music.play(-1, 0.0, 5000)
        else:
            pygame.mixer.music.unload()



def waiting_screen(waiting_screen, text1, text2, font, time, screen):
    screen.blit(waiting_screen, (0,0))
    text_width, text_height = font.size(f"{text1}")
    draw_text(f"{text1}", font, clr_white, (SCREEN_WIDTH - text_width) // 2, (SCREEN_HEIGHT - text_height) // 2, screen)
    text_width, text_height = font.size(f"{text2}")
    draw_text(f"{text2}", font, clr_white, (SCREEN_WIDTH - text_width) // 2, (SCREEN_HEIGHT - text_height) // 2 + 100, screen)
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









player = Joueur(95, SCREEN_HEIGHT - 140, numero_joueur, type_level, level)




#LANCEMENT DU JEU -----------------------------------------------------------------------------------------------------------------------------------------------

if path.exists(f"levels/level{level}_data"):
    pickle_read = open(f"levels/level{level}_data", "rb")
    world_data = pickle.load(pickle_read)
    world = World(world_data, monde)


boutons_menu = [bouton_exit, bouton_niveaux, bouton_start, bouton_create, bouton_skins]

run=True
while run:

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
            human_delay()
            menu = LEVELS
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if bouton_skins.draw(1, SCREEN) or key[pygame.K_k]:
            human_delay()
            menu = SKINS
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if bouton_create.draw(1, SCREEN) or key[pygame.K_c]:
            human_delay()
            menu = CREATE
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if bouton_start.draw(1, SCREEN) or key[pygame.K_s]:
            human_delay()
            menu = GAME
            level = 0
            game_over = 1
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            
            
    elif menu == LEVELS:

        change_music(current_music, 0)
        current_music = 0
        SCREEN.blit(img_background_menu, (0,0))
        draw_text('Levels:', font_lilitaone_60, clr_black, 140, SCREEN_HEIGHT // 2 - 200 + mouse_scroll_niveaux, SCREEN)

        if key[pygame.K_t]:
            level_win = nb_levels_main_quest
            mode_dev = True
            score = 99999
        if mode_dev:
            draw_text('Dev mode', font_ubuntu_30, clr_black, SCREEN_WIDTH * 5 // 8, SCREEN_HEIGHT * 7 // 8 + mouse_scroll_niveaux, SCREEN)

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
                human_delay()
                menu = GAME
                last_menu = LEVELS
                level = i2 
                game_over = 1

            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                text_width, text_height = font_lilitaone_80.size(str(i2 + 1))
                if i2 + 1 in mondes[4]:
                    draw_text(f"{i2 + 1}", font_lilitaone_80, clr_white, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j + mouse_scroll_niveaux, SCREEN)
                else:
                    draw_text(f"{i2 + 1}", font_lilitaone_80, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j + mouse_scroll_niveaux, SCREEN)
            else:
                text_width, text_height = font_lilitaone_70.size(str(i2 + 1))
                if i2 + 1 in mondes[4]:
                    draw_text(f"{i2 + 1}", font_lilitaone_70, clr_white, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j + mouse_scroll_niveaux, SCREEN)
                else:
                    draw_text(f"{i2 + 1}", font_lilitaone_70, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j + mouse_scroll_niveaux, SCREEN)

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
                draw_text(f"{i2 + 1}", font_lilitaone_70, clr_white_minus, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j2 + mouse_scroll_niveaux, SCREEN)
            else:
                draw_text(f"{i2 + 1}", font_lilitaone_70, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j2 + mouse_scroll_niveaux, SCREEN)
            SCREEN.blit(img_cadenas, (SCREEN_WIDTH // 2 + 140 * (i - 4) + 6, SCREEN_HEIGHT // 2 - 45 + 140 * j2 + mouse_scroll_niveaux))

        if bouton_back.draw(1, SCREEN) or key[pygame.K_ESCAPE]:
            human_delay()
            menu = MAIN
        
        if bouton_suite.draw(1, SCREEN):
            human_delay()
            menu = MINIGAMES
        
        if bouton_delete.draw(1, SCREEN):
            level_win = 1




    elif menu == MINIGAMES:


        change_music(current_music, 0)
        current_music = 0
        SCREEN.blit(img_background_menu, (0,0))
        draw_text('Mini-jeux:', font_lilitaone_60, clr_black, 140, SCREEN_HEIGHT // 2 - 200, SCREEN)
        draw_text("more soon...", font_bauhaus_50, clr_black, SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT * 5 // 6, SCREEN)

        if bouton_retour.draw(1, SCREEN):
            human_delay()
            menu = LEVELS

        if bouton_suite.draw(1, SCREEN):
            human_delay()
            menu = CREATED_LVLS

        if bouton_back.draw(1, SCREEN) or key[pygame.K_ESCAPE]:
            human_delay()
            menu = MAIN
        
        if bouton_random_mg.draw(1, SCREEN):    
            random_mg = True
            human_delay()
            menu = GAME
            last_menu = MINIGAMES
            level = 101
            game_over = 1  
        draw_text("RANDOM", font_bauhaus_40, clr_black, SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 146, SCREEN)          


        for i in range(nb_minis_jeux):
            level_num = 6

            i2 = i
            j = i // 8
            i = i % 8

            bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4), SCREEN_HEIGHT // 2 - 50 + 140 * j, 100, 100, pygame.image.load(f"sprites/img_bouton_niveau_on_{level_num}_petit.webp"))
            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                bouton_niveau = Bouton(SCREEN_WIDTH // 2 + 140 * (i - 4) - 5, SCREEN_HEIGHT // 2 - 55 + 140 * j, 110, 110, pygame.image.load(f"sprites/img_bouton_niveau_on_{level_num}_gros.webp"))

            if bouton_niveau.draw(2, SCREEN):
                human_delay()
                menu = GAME
                last_menu = MINIGAMES
                level = 100 + i2
                game_over = 1

            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                SCREEN.blit(pygame.image.load(f"sprites/img_{minigame_type[i2]}.webp"), (SCREEN_WIDTH // 2 + 140 * (i - 4) + 5, SCREEN_HEIGHT // 2 - 45 + 140 * j))
                if not number_minigame[i2] == "1":
                    draw_text(number_minigame[i2], font_lilitaone_30, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 76, SCREEN_HEIGHT // 2 - 50 + 140 * j, SCREEN)
            else:
                SCREEN.blit(pygame.image.load(f"sprites/img_{minigame_type[i2]}_petit.webp"), (SCREEN_WIDTH // 2 + 140 * (i - 4) + 5, SCREEN_HEIGHT // 2 - 45 + 140 * j))
                if not number_minigame[i2] == "1":
                    draw_text(number_minigame[i2], font_lilitaone_30, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 72, SCREEN_HEIGHT // 2 - 45 + 140 * j, SCREEN)
        



    elif menu == CREATED_LVLS:

        change_music(current_music, 0)
        current_music = 0
        SCREEN.blit(img_background_menu, (0,0))
        draw_text('Niveaux créés:', font_lilitaone_60, clr_black, 140, SCREEN_HEIGHT // 2 - 200, SCREEN)

        if key[pygame.K_t]:
            level_win = nb_levels_main_quest
            mode_dev = True
        if mode_dev:
            draw_text('mode développeur activé', font_ubuntu_30, clr_black, SCREEN_WIDTH * 5 // 8, SCREEN_HEIGHT * 7 // 8, SCREEN)

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
                human_delay()
                menu = GAME
                last_menu = CREATED_LVLS
                level = 200 + i2
                game_over = 1

            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                text_width, text_height = font_lilitaone_80.size(str(i2 + 1))
                draw_text(f"{i2 + 1}", font_lilitaone_80, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j, SCREEN)
            else:
                text_width, text_height = font_lilitaone_70.size(str(i2 + 1))
                draw_text(f"{i2 + 1}", font_lilitaone_70, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j, SCREEN)

        if bouton_back.draw(1, SCREEN) or key[pygame.K_ESCAPE]:
            human_delay()
            menu = MAIN
        
        if bouton_retour.draw(1, SCREEN):
            human_delay()
            menu = MINIGAMES




    elif menu == CREATE:

        change_music(current_music, 0)
        current_music = 0
        SCREEN.blit(img_background_menu, (0,0))
        draw_text('Vos niveaux:', font_lilitaone_60, clr_black, 140, SCREEN_HEIGHT // 2 - 200, SCREEN)

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
                level_names[i2+1] = write(level_names[i2+1], font_lilitaone_80, font_bauhaus_50, font_ubuntu_30, clr_white, "Entrez un nom pour le niveau:", 20, SCREEN)
                main(201 + i2)

            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                text_width, text_height = font_lilitaone_80.size(str(i2 + 1))
                draw_text(f"{i2 + 1}", font_lilitaone_80, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j, SCREEN)
            else:
                text_width, text_height = font_lilitaone_70.size(str(i2 + 1))
                draw_text(f"{i2 + 1}", font_lilitaone_70, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 50 - text_width // 2, SCREEN_HEIGHT // 2 - text_height // 2 + 140 * j, SCREEN)


        if bouton_add.draw(1, SCREEN) and nb_created_levels < 20:
            nb_created_levels += 1

        if bouton_delete.draw(1, SCREEN) and nb_created_levels > 1:
            nb_created_levels -= 1


        if bouton_back.draw(1, SCREEN) or key[pygame.K_ESCAPE]:
            human_delay()
            menu = MAIN




    elif menu == SKINS:

        change_music(current_music, 0)
        current_music = 0
        SCREEN.blit(img_background_menu, (0,0))
        draw_text('Galerie des skins:', font_lilitaone_60, clr_black, 140, SCREEN_HEIGHT // 2 - 200, SCREEN)
        draw_text(f'Vous avez {score} pièces', font_lilitaone_70, clr_black, SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 150, SCREEN)

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
                draw_text(f"{skin_prices[i2]}", font_lilitaone_30, clr_black, SCREEN_WIDTH // 2 + 140 * (i - 4) + 12, SCREEN_HEIGHT // 2 + 10 + 140 * j, SCREEN)
                SCREEN.blit(img_coin_price, (SCREEN_WIDTH // 2 + 140 * (i - 4) + 64, SCREEN_HEIGHT // 2 + 15 + 140 * j))


            if bouton_niveau.rect.collidepoint(pygame.mouse.get_pos()):
                SCREEN.blit(pygame.image.load("sprites/img_bouton_niveau_0_gros.webp"), (SCREEN_WIDTH // 2 + 140 * (i - 4) - 5, SCREEN_HEIGHT // 2 - 55 + 140 * j))
            else:
                SCREEN.blit(pygame.image.load("sprites/img_bouton_niveau_0.webp"), (SCREEN_WIDTH // 2 + 140 * (i - 4), SCREEN_HEIGHT // 2 - 50 + 140 * j))
            

        if bouton_back.draw(1, SCREEN) or key[pygame.K_ESCAPE]:
            human_delay()
            menu = MAIN

        if key[pygame.K_t]:
            level_win = nb_levels_main_quest
            mode_dev = True
            score = 99999 




    else:

        world.draw(SCREEN)

        change_music(current_music, monde)
        current_music = monde

        if game_over == 0:
            if lock_lines == True:
                lock_lines = False
                lock_game_over = False
            #drawwwwww un max
            full_draw(groups, SCREEN)
            game_over = player.update(game_over, type_level, SCREEN)
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
            draw_text('x ' + str(score), font_bauhaus_50, clr_black, TILE_SIZE + 350, 70, SCREEN)
            draw_text('niveau: ' + str(level), font_bauhaus_50, clr_black, TILE_SIZE + 40, 70, SCREEN)


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


        if menu == PAUSE:

            SCREEN.blit(img_background_pause, (SCREEN_WIDTH // 2 - 500, SCREEN_HEIGHT // 2 - 250))
            game_over = 2
            if bouton_resume_pause.rect.collidepoint(pygame.mouse.get_pos()) or bouton_menu_pause.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if bouton_resume_pause.draw(1, SCREEN):
                human_delay()
                game_over = 0
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if bouton_menu_pause.draw(1, SCREEN):
                human_delay()
                game_over = 0
                level = 1
                monde = 1
                random_mg = False
                player.reset(100, SCREEN_HEIGHT - 150, type_level, numero_joueur, level)
                reset_level(level, groups, player, type_level, numero_joueur)
                menu = last_menu
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if game_over == -1:
            if not lock_game_over:
                game_over_msc.play()
                lock_game_over = True
            fond_group.draw(SCREEN)
            game_over = player.update(game_over, type_level, SCREEN)
            full_draw(groups, SCREEN)
            SCREEN.blit(img_background_score, (50,50))
            SCREEN.blit(img_coin_score, (357,85))
            draw_text('x ' + str(score), font_bauhaus_50, clr_black, TILE_SIZE + 350, 70, SCREEN)
            draw_text('niveau: ' + str(level), font_bauhaus_50, clr_black, TILE_SIZE + 40, 70, SCREEN)
            SCREEN.blit(img_background_mort, (SCREEN_WIDTH // 2 - 200,SCREEN_HEIGHT // 2 - 200))
            lines = ["pfff really?","how u so bad?","skill issue?","not even close","nice death"]
            if lock_lines == False:
                random_line = random.randint(0, len(lines) - 1)
                lock_lines = True
            text_width, text_height = font_lilitaone_60.size(lines[random_line])
            draw_text(lines[random_line], font_lilitaone_60, clr_brown, SCREEN_WIDTH // 2 - text_width // 2, SCREEN_HEIGHT // 2 - 150, SCREEN)
            draw_text("press enter to restart", font_ubuntu_30, clr_brown, SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 2 + 235, SCREEN)
            if bouton_restart.rect.collidepoint(pygame.mouse.get_pos()) or bouton_menu.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if bouton_restart.draw(1, SCREEN) or key[pygame.K_RETURN]:
                human_delay()
                player.mostleftposition = 0
                world_data = []
                world = reset_level(level, groups, player, type_level, numero_joueur)
                game_over = 0
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if bouton_menu.draw(1, SCREEN):
                human_delay()
                menu = last_menu
                game_over = 0
                level = 1
                monde = 1
                random_mg = False
                world = reset_level(1, groups, player, type_level, numero_joueur)
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
                world = reset_level(level, groups, player, type_level, numero_joueur)

            else:
                msg=["MINH", "DOAN"]
                draw_text(f'TU AS TROUVE {msg[numero_joueur - 1]}!', font_lilitaone_60, clr_blue, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 170, SCREEN)
                if bouton_restart.draw(1, SCREEN) or key[pygame.K_RETURN] == True:
                    menu = last_menu
                    player.direction = 1
                    level = 1
                    monde = 1
                    world = reset_level(level, groups, player, type_level, numero_joueur)
                    game_over = 0

        #draw_grid()

    pygame.display.update()


pygame.quit()