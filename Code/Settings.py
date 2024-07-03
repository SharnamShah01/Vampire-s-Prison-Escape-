import pygame
from pytmx.util_pygame import load_pygame
from os.path import join

WIN_WIDTH,WIN_HEIGHT = 1200,650
INT_SURF_SIZE = (2500,1500)

TILE_SIZE = 64

BG_COLOR = '#4F3A60'

scale_factor = 2

# player
PLAYER_SPEED = 300
Scale_image_by = 1.5



# Enemy
ENEMY_SPEED = 200
ENEMY_SPAWN_RATE = 600

# Dungeon
DUN_TILE_SIZE = 32

KEY_IMAGE = pygame.Surface((16,16))
DUN_ENEMY_SPAWN_RATE = 2000
DUN_ENEMY_SPEED = 50

