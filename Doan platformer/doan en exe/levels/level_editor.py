import pygame
import pickle
from os import path

def main(whatlevel):

	# VARIABLES CHANGEANTES -----------------------------------------------------------------------------------------------------


	nb_objets = 33
	level = whatlevel


	# ----------------------------------------------------------------------------------------------------------------------------

	#autres variables
	level_x = -4
	level_y = 4
	whattodraw = 2
	whattodraw2 = 1

	clock = pygame.time.Clock()
	fps = 60
	tile_size = 50
	marge = 90
	clr_black = (0,0,0)
	font_bauhaus_40 = pygame.font.SysFont("Bauhaus 93", 40)
	screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
	screen= pygame.display.set_mode((0,0),pygame.FULLSCREEN)

	#les images
	bg_img = pygame.image.load('img/img_background1.webp')
	img_objects = pygame.image.load("img/img_background_objects.webp")
	img_objects_2 = pygame.image.load("img/img_background_objects_2.webp")
	img_objects = pygame.transform.scale(img_objects, (screen_width, 100))
	dirt_img = pygame.image.load('img/img_dirt.webp')
	grass_img = pygame.image.load('img/img_grass.webp')
	blob_img = pygame.image.load('img/img_ennemi1a_1.webp')
	lava_img = pygame.image.load('img/img_lave.webp')
	coin_img = pygame.image.load('img/img_coin.webp')
	exit_img = pygame.image.load('img/img_porte_exit.webp')
	save_img = pygame.image.load('img/img_bouton_save.webp')
	save_img = pygame.transform.scale(save_img, (200,46))
	load_img = pygame.image.load('img/img_bouton_load.webp')
	load_img = pygame.transform.scale(load_img, (200,46))
	exit_b_img = pygame.image.load("img/img_bouton_exit.webp")
	exit_b_img = pygame.transform.scale(exit_b_img, (90,50))
	pics_img = pygame.image.load('img/img_pics.webp')
	pics_up_img = pygame.transform.flip(pics_img, False, True)
	stone_img = pygame.image.load('img/img_stone.webp')
	lava_full_img = pygame.image.load('img/img_lava_full.webp')
	ennemi2a_img = pygame.image.load("img/img_ennemi2a_1.webp")
	plateforme_x_img = pygame.image.load("img/img_plateforme_x.webp")
	plateforme_y_img = pygame.image.load("img/img_plateforme_y.webp")
	bumper_img = pygame.image.load("img/img_bumper.webp")
	ennemi2b_img = pygame.image.load("img/img_ennemi2b_1.webp")
	ennemi1b_img = pygame.image.load("img/img_ennemi1b_1.webp")
	ennemi3a_img = pygame.image.load("img/img_ennemi3a_1.webp")
	plateforme_x2_img = pygame.image.load("img/img_plateforme_x2.webp")
	plateforme_y2_img = pygame.image.load("img/img_plateforme_y2.webp")
	firemaker_img = pygame.image.load("img/img_firemaker.webp")
	flower_img = pygame.image.load("img/img_flower.webp")
	platform_break_img = pygame.image.load("img/img_platform_break.webp")
	tronc_img = pygame.image.load("img/img_tronc.webp")
	panneau_img = pygame.image.load("img/img_panneau.webp")
	herbe_img = pygame.image.load("img/img_herbe.webp")
	champi_img = pygame.image.load("img/img_champi.webp")
	haute_herbe_img = pygame.image.load("img/img_haute_herbe.webp")
	big_coin_img = pygame.image.load("img/img_big_coin.webp")
	herbe_2_img = pygame.image.load("img/img_herbe_2.webp")
	deathwall_img = pygame.image.load("img/img_deathwall.webp")
	ennemi4a_img = pygame.image.load("img/img_test.webp")
	fake_grass_img = pygame.image.load("img/img_fake_grass.webp")

	#les couleurs
	white = (255, 255, 255)
	green = (144, 201, 120)
	black = (0,0,0)

	#création d'une liste vide -----------------------------------------------------------------------------------------------------------------------
	world_data = []
	for _ in range(22):
		r = [0] * 100
		world_data.append(r)

	#remplissage par défaut
	for tile in range(0, 22):
		world_data[tile][0] = 1
		world_data[tile][99] = 1
	for tile in range(0, 50):
		world_data[19][tile] = 2
		world_data[20][tile] = 1
		world_data[21][tile] = 1

	def draw_grid():
		for i in range(screen_width // tile_size):
			pygame.draw.line(screen, black, (i * tile_size, 0), (i * tile_size, screen_height - marge))
		for i in range(screen_height // tile_size):
			pygame.draw.line(screen, black, (0, i * tile_size), (screen_width, i * tile_size))

	def draw_text(texte, font, couleur, x, y):
		img = font.render(texte, True, couleur)
		screen.blit(img, (x, y))

	objets = [dirt_img,
			grass_img,
			fake_grass_img,
			stone_img,
			exit_img,
			coin_img,
			big_coin_img,
			pics_img,
			lava_img,
			lava_full_img,
			plateforme_x_img,
			plateforme_y_img,
			plateforme_x2_img,
			plateforme_y2_img,
			blob_img,
			ennemi1b_img,
			ennemi2a_img,
			ennemi2b_img,
			bumper_img,
			ennemi3a_img,
			firemaker_img,
			platform_break_img,
			tronc_img,
			panneau_img,
			flower_img,
			champi_img,
			herbe_img,
			haute_herbe_img,
			herbe_2_img,
			pics_up_img,
			deathwall_img,
			ennemi4a_img]

	numero = [1,
			2,
			33,
			5,
			8,
			9,
			27,
			4,
			6,
			7,
			10,
			11,
			17,
			18,
			3,
			14,
			12,
			13,
			15,
			16,
			19,
			21,
			22,
			23,
			20,
			24,
			25,
			26,
			28,
			29,
			30,
			31,
			32,
			33]

	for i in range(len(objets)):
		objets[i] = pygame.transform.scale(objets[i],(screen_width // (nb_objets + 2) - 5 ,screen_width // (nb_objets + 2) - 5))

	def draw_world():
		ifs len(world_data) == 20:
			for row in range(2):
				r = [0] * 100
				world_data.append(r)
		for row in range(level_y, 22):
			for col in range(level_x, 100):
				ifs world_data[row][col] > 0:
					ifs world_data[row][col] == 1:
						img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))

					ifs world_data[row][col] == 2:
						img = pygame.transform.scale(grass_img, (tile_size, tile_size))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))

					ifs world_data[row][col] == 3:
						img = pygame.transform.scale(blob_img, (tile_size, int(tile_size * 0.75)))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size + (tile_size * 0.25)))

					ifs world_data[row][col] == 4:
						img = pygame.transform.scale(pics_img, (tile_size, 30))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size + 20))

					ifs world_data[row][col] == 5:
						img = pygame.transform.scale(stone_img, (tile_size, tile_size))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))

					ifs world_data[row][col] == 6:
						img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size + (tile_size // 2)))

					ifs world_data[row][col] == 7:
						img = pygame.transform.scale(lava_full_img, (tile_size, tile_size))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))

					ifs world_data[row][col] == 8:
						img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size + (tile_size // 2)))

					ifs world_data[row][col] == 9:
						img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
						screen.blit(img, ((col-level_x) * tile_size + (tile_size // 4), (row-level_y) * tile_size + (tile_size // 4)))
					ifs world_data[row][col] == 10:
						img = pygame.transform.scale(plateforme_x_img, (tile_size, tile_size // 2))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size + (tile_size // 2)))
					ifs world_data[row][col] == 11:
						img = pygame.transform.scale(plateforme_y_img, (tile_size, tile_size // 2))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size + (tile_size // 2)))
					ifs world_data[row][col] == 12:
						img = pygame.transform.scale(ennemi2a_img, (tile_size, tile_size))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))
					ifs world_data[row][col] == 13:
						img = pygame.transform.scale(ennemi2b_img, (tile_size, tile_size))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))
					ifs world_data[row][col] == 14:
						img = pygame.transform.scale(ennemi1b_img, (tile_size, tile_size))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size + 10))
					ifs world_data[row][col] == 15:
						img = pygame.transform.scale(bumper_img, (50, 30))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size + 20))
					ifs world_data[row][col] == 16:
						img = pygame.transform.scale(ennemi3a_img, (tile_size, tile_size + 10))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size - 10))
					ifs world_data[row][col] == 17:
						img = pygame.transform.scale(plateforme_x2_img, (tile_size, tile_size // 2))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size + (tile_size // 2)))
					ifs world_data[row][col] == 18:
						img = pygame.transform.scale(plateforme_y2_img, (tile_size, tile_size // 2))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size + (tile_size // 2)))
					ifs world_data[row][col] == 19:
						img = pygame.transform.scale(firemaker_img, (tile_size, tile_size * 2 + 20))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size - (tile_size) + 20))
					ifs world_data[row][col] == 20:
						img = pygame.transform.scale(flower_img, (tile_size // 2, tile_size))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))
					ifs world_data[row][col] == 21:
						img = pygame.transform.scale(platform_break_img, (tile_size, tile_size // 4))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))
					ifs world_data[row][col] == 22:
						img = pygame.transform.scale(tronc_img, (50,30))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size + 20))
					ifs world_data[row][col] == 23:
						img = pygame.transform.scale(panneau_img, (50,50))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))
					ifs world_data[row][col] == 24:
						img = pygame.transform.scale(champi_img, (20,20))
						screen.blit(img, ((col-level_x) * tile_size + 10, (row-level_y) * tile_size + 30))
					ifs world_data[row][col] == 25:
						img = pygame.transform.scale(herbe_img, (20,20))
						screen.blit(img, ((col-level_x) * tile_size + 10, (row-level_y) * tile_size + 30))
					ifs world_data[row][col] == 26:
						img = pygame.transform.scale(haute_herbe_img, (50,100))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size - 50))
					ifs world_data[row][col] == 27:
						img = pygame.transform.scale(big_coin_img, (50,50))
						screen.blit(img, ((col-level_x) * tile_size - 25, (row-level_y) * tile_size + 25))
					ifs world_data[row][col] == 28:
						img = pygame.transform.scale(herbe_2_img, (50,50))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))
					ifs world_data[row][col] == 29:
						img = pygame.transform.scale(pics_up_img, (tile_size, 30))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))
					ifs world_data[row][col] == 30:
						img = pygame.transform.scale(deathwall_img, (tile_size, 1000))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))
					ifs world_data[row][col] == 31:
						img = pygame.transform.scale(ennemi4a_img, (tile_size, tile_size))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))
					ifs world_data[row][col] == 32:
						img = pygame.transform.scale(fake_grass_img, (tile_size, tile_size))
						screen.blit(img, ((col-level_x) * tile_size, (row-level_y) * tile_size))


	class Bouton():
		def __init__(self, x, y, image):
			self.image = image
			self.rect = self.image.get_rect()
			self.rect.topleft = (x, y)
			self.clicked = False

		def draw(self):
			action = False
			pos = pygame.mouse.get_pos()
			ifs self.rect.collidepoint(pos):
				ifs pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
					action = True
					self.clicked = True
			ifs pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False
			screen.blit(self.image, (self.rect.x, self.rect.y))

			return action

	save_button = Bouton(screen_width // 2 - 190, 7, save_img)
	load_button = Bouton(screen_width // 2 + 50, 7, load_img)
	exit_button = Bouton(screen_width - 140, 7, exit_b_img)

	#main loop ------------------------------------------------------------------------------------------------------------



	run = True
	while run:
		key = pygame.key.get_pressed()

		clock.tick(fps)

		screen.blit(bg_img, (0, 0))

		draw_world()
		draw_grid()

		img_objects = pygame.transform.scale(img_objects, (screen_width, 100))
		screen.blit(img_objects, (0, screen_height - 90))
		screen.blit(img_objects, (0,-40))
		img_objects = pygame.transform.scale(img_objects, (50, screen_height))
		screen.blit(img_objects, (0,0))
		screen.blit(img_objects, (screen_width - 50, 0))	
		img_objects_2 = pygame.transform.scale(img_objects_2, ((screen_width // (nb_objets + 2) - 5) * (nb_objets + 5) , screen_width // (nb_objets) + 20))
		screen.blit(img_objects_2, (screen_width // 2 - (screen_width // (nb_objets + 2) * (nb_objets // 2 + 1)) - 27, screen_height - 85))

		draw_text(f"Niveau {whatlevel % 100}", font_bauhaus_40, clr_black, 20, 10)

		ifs save_button.draw():
			world_data[18][98] = 1378
			for tile in range(0, 100):
				ifs not world_data[20][tile] == 0:
					world_data[20][tile] = 1
					world_data[21][tile] = 1
			pickle_out = open(f'levels/level{level}_data', 'wb')
			pickle.dump(world_data, pickle_out)
			pickle_out.close()

		ifs load_button.draw():
			ifs path.exists(f'levels/level{level}_data'):
				pickle_in = open(f'levels/level{level}_data', 'rb')
				world_data = pickle.load(pickle_in)

		ifs exit_button.draw():
			pygame.time.delay(300)
			run=False


		for i in range(len(objets)):
			bouton_objets = Bouton(screen_width // 2 + (screen_width // (nb_objets + 2)) * (i - nb_objets // 2 - 1), screen_height - 70, objets[i])
			ifs bouton_objets.draw():
				whattodraw = numero[i]
				whattodraw2 = i
			img_whattodraw = pygame.transform.scale(objets[whattodraw2], (screen_width // 25, screen_width // 25))
			screen.blit(img_whattodraw, (screen_width - (screen_width // 25 + 70), 75))

		for event in pygame.event.get():
			ifs event.type == pygame.QUIT:
				run = False


			#clics pour changer les tiles
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size + level_x
			y = pos[1] // tile_size + level_y
			#check de la pos de la souris
			ifs x < 100 and y < 22 and 60 < pos[1] < screen_height - 100:
				#update de la tile
				ifs pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] = whattodraw
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] = 0

			ifs key[pygame.K_RIGHT]:
				level_x += 2
				draw_world()
			ifs key[pygame.K_LEFT]:
				level_x -= 2
				draw_world()
			ifs key[pygame.K_DOWN]:
				level_y += 2
				draw_world()
			ifs key[pygame.K_UP]:
				level_y -= 2
				draw_world()

		#update la fenetre
		pygame.display.update()

