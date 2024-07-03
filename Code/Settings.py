import pygame
from pytmx.util_pygame import load_pygame
from os.path import join

WIN_WIDTH,WIN_HEIGHT = 1200,650
INT_SURF_SIZE = (2500,1500)

TILE_SIZE = 64

BG_COLOR = '#4F3A60'

scale_factor = 2

# player
PLAYER_SPEED = 200
Scale_image_by = (20,27.5)
PLAYER_HEALTH = 50
PLAYER_DAMAGE = 5
PLAYER_ATTACK_COOLDOWN = 100

# forest:

# Enemy
ENEMY_SPEED = 200
ENEMY_SPAWN_RATE = 600
ENEMY_DAMAGE = 10
ENEMY_HEALTH = 15
ENEMY_ATTACK_COOLDOWN = 450

# Dungeon
DUN_TILE_SIZE = 32

KEY_IMAGE = pygame.Surface((16,16))
DUN_ENEMY_SPAWN_RATE = 2000
DUN_ENEMY_SPEED = 100
DUN_ENEMY_HEALTH = 10
DUN_ENEMY_DAMAGE = 2
DUN_ATTACK_COOLDOWN = 400

key_font_type = None
key_font_size = 50
key_disp_place = (100,100)
Key_font_collor = 'yellow'

