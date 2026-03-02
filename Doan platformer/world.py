from imports import *
from functions import *
from constants import *

def reset_level(level, groups, player, type_level, numero_joueur):
    player.reset(100, SCREEN_HEIGHT - 150, type_level, numero_joueur, level)
    for group in groups:
        group.empty()
    world_data = []
    if path.exists(f"levels/level{level}_data"):
        pickle_read = open(f"levels/level{level}_data", "rb")
        world_data = pickle.load(pickle_read)
        world = World(world_data)
    return world

class World():
    def __init__(self, data, monde=1):
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

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
