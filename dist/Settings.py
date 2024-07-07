import pygame
from pytmx.util_pygame import load_pygame
from os.path import join
import json

WIN_WIDTH,WIN_HEIGHT = 1200,650
INT_SURF_SIZE = (2500,1500)

TILE_SIZE = 64

FOREST_TILE_SIZEE = 16

BG_COLOR = '#4F3A60'




# instruction
instruc_font = join('assests' ,'Font' , 'INTRU_FONT.ttf')
instruc_font_size = 50
instru_font_color = 'white'
instru_pos = (WIN_WIDTH/2 -500,WIN_HEIGHT/2+100)
instru_bg_color = None

forest_instru_color = 'black'


# player
PLAYER_SPEED = 200
Scale_image_by = (20,27.5)
PLAYER_HEALTH = 50
PLAYER_DAMAGE = 5

PLAYER_PUNCH_COOLDOWN = 125

PLAYER_BLOOD_COOLDDOWN = 500
BLOOD_THROW_SPEED = 250
BLOOD_THROW_DAMAGE = 3


PLAYER_HEALTH_FONT = join('assests' ,'Font' , 'geek.ttf')
PLAYER_FONT_SIZE = 40
PLAYER_HEALTH_FONT_POS = (100,30)
PLAYER_HEALTH_COLOR = 'white'


BAT_TIME = 3000
BAT_COOLDOWN = 3000

# forest:
TIME_IN_FOREST = 30000

# Enemy
DINO_ENEMY_SPEED = 200
DINO_ENEMY_SPAWN_RATE = 1200
DINO_ENEMY_DAMAGE = 10
DINO_ENEMY_HEALTH = 15
DINO_ENEMY_ATTACK_COOLDOWN = 450

# Dungeon
DUN_TILE_SIZE = 32

KEY_IMAGE = pygame.Surface((16,16))
DUN_ENEMY_SPAWN_RATE = 1250
DUN_ENEMY_SPEED = 100
DUN_ENEMY_HEALTH = 10
DUN_ENEMY_DAMAGE = 2
DUN_ATTACK_COOLDOWN = 400


# keys
key_font_type = join('assests' ,'Font' , 'geek.ttf')
key_font_size = 50
key_disp_place = (100,100)
Key_font_collor = 'yellow'



# end screen
END_SCREEN_BG_COLOR = 'black'
END_SCREEN_FONT = None
END_FONT_SIZE = 50
END_FONT_POOS = (WIN_WIDTH/2-150,WIN_HEIGHT/2-150)
END_SCREEN_COLOR = 'black'
END_SCREEN_BG = pygame.image.load(join('assests' ,'images' , 'Backgrounds' , 'end_screen_bg.bmp'))



# title screen
TITLE_SCREEN_pos = (WIN_WIDTH/2,WIN_HEIGHT/2+3)
TITLE_SCREEN_FONT = join('assests' ,'Font', 'TITLE_SCREEN_FONT.ttf')
TITLE_SCREEN_FONT_SIZE = 80
TITLE_SCREEN_FONT_POS = (WIN_WIDTH/2-200,WIN_HEIGHT/2)
TITLE_SCREEN_PLAY_POS = (WIN_WIDTH/2-200,WIN_HEIGHT/2+100)
TITLE_COLOR = 'gold'
PLAY_COLOR = 'black'



# DEATH SCREEN
DEATH_FONT = join('assests' ,'Font', 'DEATH_FONT.ttf')
DEATH_FONT_SIZE = 100
DEATH_FONT_POS = (WIN_WIDTH/2,WIN_HEIGHT/2)
DEATH_FONT_COLOR = 'red'


# Between SCREEN
BET_SCREEN_FONT_FILE = None
BET_FONT_SIZE = 50
BET_FONT_POS = (WIN_WIDTH/2,WIN_HEIGHT/2)
BET_FONT_COLOR = 'white'
BET_IMAGE = pygame.image.load(join('assests' ,'Data' , 'BET' , 'bet.png'))


# story
STORY_FONT = join('assests' ,'Font' , 'AngerStyles.ttf')
STORY_FONT_SIZE = 50
STORY_FONT_COLOR = 'black'

