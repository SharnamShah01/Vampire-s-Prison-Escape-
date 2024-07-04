import pygame
from pytmx.util_pygame import load_pygame
from os.path import join

WIN_WIDTH,WIN_HEIGHT = 1200,650
INT_SURF_SIZE = (2500,1500)

TILE_SIZE = 64

FOREST_TILE_SIZEE = 16

BG_COLOR = '#4F3A60'




# instruction
instruc_font = None
instruc_font_size = 30
instru_font_color = 'green'
instru_pos = (WIN_WIDTH/2 ,WIN_HEIGHT/2)
instru_bg_color = None


# player
PLAYER_SPEED = 200
Scale_image_by = (20,27.5)
PLAYER_HEALTH = 50
PLAYER_DAMAGE = 5

PLAYER_PUNCH_COOLDOWN = 125

PLAYER_BLOOD_COOLDDOWN = 500
BLOOD_THROW_SPEED = 250
BLOOD_THROW_DAMAGE = 3


PLAYER_HEALTH_FONT = None
PLAYER_FONT_SIZE = 40
PLAYER_HEALTH_FONT_POS = (100,30)
PLAYER_HEALTH_COLOR = 'white'


BAT_TIME = 3000
BAT_COOLDOWN = 3000

# forest:

# Enemy
DINO_ENEMY_SPEED = 200
DINO_ENEMY_SPAWN_RATE = 1200
DINO_ENEMY_DAMAGE = 10
DINO_ENEMY_HEALTH = 15
DINO_ENEMY_ATTACK_COOLDOWN = 450

# Dungeon
DUN_TILE_SIZE = 32

KEY_IMAGE = pygame.Surface((16,16))
DUN_ENEMY_SPAWN_RATE = 1750
DUN_ENEMY_SPEED = 100
DUN_ENEMY_HEALTH = 10
DUN_ENEMY_DAMAGE = 2
DUN_ATTACK_COOLDOWN = 400

key_font_type = None
key_font_size = 50
key_disp_place = (100,100)
Key_font_collor = 'yellow'

