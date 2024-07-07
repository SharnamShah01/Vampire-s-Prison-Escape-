import pygame
import asyncio
# from Settings import *
# from Sprites import *
# from Groups import *
from random import choice
from pytmx.util_pygame import load_pygame
from os.path import join
import json

WIN_WIDTH,WIN_HEIGHT = 1200,650
INT_SURF_SIZE = (2500,1500)

TILE_SIZE = 64

FOREST_TILE_SIZEE = 16

BG_COLOR = '#4F3A60'




# instruction
instruc_font = join('Font' , 'INTRU_FONT.ttf')
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


PLAYER_HEALTH_FONT = join('Font' , 'geek.ttf')
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
key_font_type = join('Font' , 'geek.ttf')
key_font_size = 50
key_disp_place = (100,100)
Key_font_collor = 'yellow'



# end screen
END_SCREEN_BG_COLOR = 'black'
END_SCREEN_FONT = None
END_FONT_SIZE = 50
END_FONT_POOS = (WIN_WIDTH/2-150,WIN_HEIGHT/2-150)
END_SCREEN_COLOR = 'black'
END_SCREEN_BG = pygame.image.load(join('images' , 'Backgrounds' , 'end_screen_bg.bmp'))



# title screen
TITLE_SCREEN_pos = (WIN_WIDTH/2,WIN_HEIGHT/2+3)
TITLE_SCREEN_FONT = join('Font', 'TITLE_SCREEN_FONT.ttf')
TITLE_SCREEN_FONT_SIZE = 80
TITLE_SCREEN_FONT_POS = (WIN_WIDTH/2-200,WIN_HEIGHT/2)
TITLE_SCREEN_PLAY_POS = (WIN_WIDTH/2-200,WIN_HEIGHT/2+100)
TITLE_COLOR = 'gold'
PLAY_COLOR = 'black'



# DEATH SCREEN
DEATH_FONT = join('Font', 'DEATH_FONT.ttf')
DEATH_FONT_SIZE = 100
DEATH_FONT_POS = (WIN_WIDTH/2,WIN_HEIGHT/2)
DEATH_FONT_COLOR = 'red'


# Between SCREEN
BET_SCREEN_FONT_FILE = None
BET_FONT_SIZE = 50
BET_FONT_POS = (WIN_WIDTH/2,WIN_HEIGHT/2)
BET_FONT_COLOR = 'white'
BET_IMAGE = pygame.image.load(join('Data' , 'BET' , 'bet.png'))


# story
STORY_FONT = join('Font' , 'AngerStyles.ttf')
STORY_FONT_SIZE = 50
STORY_FONT_COLOR = 'black'


class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = (pos))

class TREESprtite(pygame.sprite.Sprite):
    def __init__(self,groups,pos,image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(topleft = pos)

class BloodThrow(pygame.sprite.Sprite):
    def __init__(self,pos,groups,player):
        super().__init__(groups)
        self.image = pygame.image.load(join('images','Vampire', 'blood charge','down','0.png'))
        self.rect = self.image.get_frect(center = pos)
        
        self.speed = BLOOD_THROW_SPEED
        self.spawn_time= pygame.time.get_ticks()
        self.lifetime = 2000
        self.frames =0  
        self.folder = ''

        if player.direction.x> 0:
            self.folder = 'right'
        if player.direction.x < 0:
            self.folder = 'left'
        if player.direction.y < 0:
            self.folder = 'up'
        if player.direction.y > 0:
            self.folder = 'down'
        
        if player.direction.x == 0 and player.direction.y ==0:
            if player.folder == 'stand up':
                self.folder = 'up'
            if player.folder == 'stand right':
                self.folder = 'right'
            if player.folder == 'stand down':
                self.folder = 'down'
            if player.folder == 'stand left':
                self.folder = 'left'
            if player.folder == 'bat':
                self.folder = 'up'



    def animate(self,dt):
        

        self.frames += 5*dt
        self.image = pygame.image.load(join('images','Vampire', 'blood charge',self.folder,f'{int(self.frames % 3)}.png'))
        self.rect = self.image.get_frect(center = self.rect.center)


    def move(self,dt):

        if self.folder == 'right':
            self.rect.x += self.speed*dt
        if self.folder == 'left':
            self.rect.x -= self.speed*dt
        if self.folder == 'down':
            self.rect.y += self.speed*dt
        if self.folder == 'up':
            self.rect.y -= self.speed*dt
        if self.folder == 'bat':
            self.rect.x += self.speed*dt

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()


    def update(self,dt):
        self.move(dt)
        self.animate(dt)
        
class DinoSprite(pygame.sprite.Sprite):
    def __init__(self,groups,pos,player,collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'Dino', 'left','0.png'))
        self.pos = choice(pos)
        self.rect = self.image.get_frect(center = self.pos)

        self.direction = pygame.Vector2()
        self.player = player
        self.speed = DINO_ENEMY_SPEED
        self.damage = DINO_ENEMY_DAMAGE
        self.health = DINO_ENEMY_HEALTH
        self.prev_attack = 0
        self.cooldown = DINO_ENEMY_ATTACK_COOLDOWN
        self.frames = 0

        self.collison_sprites = collision_sprites
        

    def get_direction(self):
        self.player_pos = pygame.Vector2(self.player.rect.center)
        self.Dino_direction = pygame.Vector2(self.rect.center)

        self.direction = (self.player_pos - self.Dino_direction).normalize()

    def move(self,dt):

        if self.player.is_bat == False:
            self.rect.x += self.speed*self.direction.x*dt
            self.collision('horizontal')
            self.rect.y += self.speed*self.direction.y*dt
            self.collision('vertical')

    def animate(self,dt):
        if self.direction.x > 0:
            self.folder = 'right'
        if self.direction.x <= 0:
            self.folder = 'left'

        self.frames += 5*dt
        self.image = pygame.image.load(join('images', 'Dino', self.folder,f'{int(self.frames%3)}.png'))
        self.rect = self.image.get_frect(center = self.rect.center)

    def collision(self,direction):
        for sprite in self.collison_sprites:
            if pygame.sprite.collide_rect(self,sprite):
                if direction == 'horizontal':
                    if self.direction.x> 0 :self.rect.right = sprite.rect.left
                    if self.direction.x <0: self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y <0: self.rect.top = sprite.rect.bottom
                    if self.direction.y >0: self.rect.bottom = sprite.rect.top

    def update(self,dt):
        self.get_direction()
        self.move(dt)
        self.animate(dt)
           
class PlayerSprite(Sprite):
    def __init__(self,pos,groups,collsion_sprtie,enemy_sprites,forest):
        self.folder = 'stand down'
        self.image = pygame.image.load(join('images', 'Vampire', self.folder, '0.png')).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image,Scale_image_by).convert_alpha()
        super().__init__(pos,self.image,groups)
        self.enemy_sprite_group = enemy_sprites
        self.collision_sprite = collsion_sprtie
        self.frames_index = 0
        self.forest = forest
        
        # powers
        self.health = PLAYER_HEALTH
        self.damage = PLAYER_DAMAGE

        self.punch_prev = 0

        self.Blood_throw = False
        self.Blood_cooldown = PLAYER_BLOOD_COOLDDOWN
        self.prev_blood_throw = 0


        # direction
        self.direction = pygame.Vector2()
        self.speed = PLAYER_SPEED

        self.prev_dir = pygame.Vector2()

        self.turn_to_bat = True
        self.time_to_remain_bat =BAT_TIME
        self.bat_cooldown = BAT_COOLDOWN
        self.bat_at_time =0
        self.bat_request = False
        self.is_bat = False
        
    def animate(self,dt):
        if self.direction.y >0:
            self.folder = 'down'

        if self.direction.y <0:
            self.folder = 'up'
            
        if self.direction.x >0:
            self.folder = 'right'

        if self.direction.x<0:
            self.folder = 'left'

        if self.direction.y == 0 and self.direction.x ==0:
            
            if self.folder == 'up':
                self.folder ='stand up'
            if self.folder == 'down':
                self.folder = 'stand down'
            if self.folder == 'right':
                self.folder = 'stand right'
            if self.folder == 'left':
                self.folder = 'stand left'

            
        if self.bat_request == True and self.turn_to_bat == True:
            if pygame.time.get_ticks() - self.bat_at_time <= self.time_to_remain_bat:
                self.folder = 'bat'
                self.is_bat = True
                
            if pygame.time.get_ticks() - self.bat_at_time > self.time_to_remain_bat:
                self.bat_at_time = pygame.time.get_ticks()
                self.bat_request = False
                self.turn_to_bat = False
                self.folder = 'down'
                self.is_bat = False


        self.frames_index += dt*5
        self.image = pygame.image.load(join('images', 'Vampire', self.folder, f'{int(self.frames_index%5)}.png'))
        self.image = pygame.transform.smoothscale(self.image,Scale_image_by).convert_alpha()
        self.rect = self.image.get_frect(center = self.rect.center)
            
    def input(self):
        keys = pygame.key.get_pressed()
        button = pygame.mouse.get_pressed()
        
        self.prev_dir.x = self.direction.x
        self.direction.x = (int(keys[pygame.K_d]) or int(keys[pygame.K_RIGHT])) - (int(keys[pygame.K_a]) or int(keys[pygame.K_LEFT]))
        self.prev_dir.y = self.direction.y
        self.direction.y = (int(keys[pygame.K_s]) or int(keys[pygame.K_DOWN])) - (int(keys[pygame.K_w]) or int(keys[pygame.K_UP]))

        self.direction = self.direction.normalize() if self.direction else self.direction

        if (keys[pygame.K_t] or button[1]) and self.turn_to_bat == True:
            self.bat_request = True
            self.bat_at_time = pygame.time.get_ticks()
            
    def move(self,dt):
        self.rect.x += self.direction.x*self.speed*dt
        self.collsions('horizontal')
        self.rect.y += self.direction.y*self.speed*dt
        self.collsions('vertical')

    def collsions(self,direction):
        for sprite in self.collision_sprite:
            if pygame.sprite.collide_mask(self,sprite):            #sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x> 0 :self.rect.right = sprite.rect.left
                    if self.direction.x <0: self.rect.left = sprite.rect.right
                else:
                    if self.direction.y <0: self.rect.top = sprite.rect.bottom
                    if self.direction.y >0: self.rect.bottom = sprite.rect.top
    
    def player_punch(self):
        key_inputs = pygame.key.get_pressed()
        mouse_inputs = pygame.mouse.get_pressed()

        if (key_inputs[pygame.K_e] or mouse_inputs[0]) and pygame.time.get_ticks() - self.punch_prev>= PLAYER_PUNCH_COOLDOWN :
                punch_soun = pygame.mixer.Sound(join('sound','punch.mp3'))
                punch_soun.play()

        for sprite in self.enemy_sprite_group:
            sprite_rect = sprite.rect.inflate(1.5,1.5)
            sprite.rect = sprite_rect
            if pygame.sprite.collide_rect(self,sprite):
                if (key_inputs[pygame.K_e] or mouse_inputs[0]) and pygame.time.get_ticks() - self.punch_prev>= PLAYER_PUNCH_COOLDOWN :
                    sprite.health -= self.damage
                    self.punch_prev = pygame.time.get_ticks()
                    if sprite.health <=0:
                        sprite.kill()
                        if self.forest == True:
                            dino_death = pygame.mixer.Sound(join('sound', 'dino died sound.mp3'))
                            dino_death.play()
                            
                        if self.forest == False:
                            DUN = pygame.mixer.Sound(join('sound' , 'dun death.mp3'))
                            DUN.play()
                    
                elif pygame.time.get_ticks() - sprite.prev_attack >= sprite.cooldown and self.is_bat == False:
                    self.health -= sprite.damage
                    self.health = max(0,self.health)
                    sprite.prev_attack = pygame.time.get_ticks()
                    dun_enemy_sound = pygame.mixer.Sound(join('sound', 'Dun enemy death.mp3'))
                    dun_enemy_sound.play()
                    
    def health_bar(self,display_at):
        if self.forest == True:
            PLAYER_HEALTH_COLOR = 'black'
        if self.forest == False:
            PLAYER_HEALTH_COLOR = 'white'


        ratio = self.health/PLAYER_HEALTH
        health_font = pygame.font.Font(PLAYER_HEALTH_FONT,PLAYER_FONT_SIZE)
        health_surf = health_font.render('Health',True,PLAYER_HEALTH_COLOR)
        health_rect = health_surf.get_frect(topleft = PLAYER_HEALTH_FONT_POS)
        display_at.blit(health_surf,health_rect)
        pygame.draw.rect(display_at, 'red' , (250,38,100,5))
        pygame.draw.rect(display_at, 'green' , (250,38,100*ratio,5))


        bat_ratio = min((pygame.time.get_ticks() - self.bat_at_time)/self.bat_cooldown,1)
        bat_surf = health_font.render('Bat Power',True,PLAYER_HEALTH_COLOR)
        bat_rect = bat_surf.get_frect(topleft = (PLAYER_HEALTH_FONT_POS[0],PLAYER_HEALTH_FONT_POS[1] + 34))
        display_at.blit(bat_surf,bat_rect)
        pygame.draw.rect(display_at, 'white' , (334,72,100,5))
        pygame.draw.rect(display_at, 'blue' , (334,72,100*bat_ratio,5))

    

    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.player_punch()

        
        if self.turn_to_bat == False:
            if pygame.time.get_ticks() - self.bat_at_time >= self.bat_cooldown:
                self.turn_to_bat = True

class TreeSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

class DoorSprite(Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(pos,surf,groups)

class ChestSprite(pygame.sprite.Sprite):
    def __init__(self,pos,image,groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(topleft = pos)
     
class GuardSprite(Sprite):
    def __init__(self,pos,image,groups,player,collision_sprites):
        super().__init__(pos,image,groups)
        self.direction = pygame.Vector2()
        self.player = player
        self.collision_sprites = collision_sprites

        # power GUARD
        self.health = DUN_ENEMY_HEALTH
        self.damage = DUN_ENEMY_DAMAGE
        self.cooldown = DUN_ATTACK_COOLDOWN
        self.prev_attack =0

        self.frame_index=0

    def move(self,dt):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()

        if self.player.is_bat == False:
            self.rect.x += self.direction.x*dt*DUN_ENEMY_SPEED
            self.collisions('horizontal')
            self.rect.y += self.direction.y*dt*DUN_ENEMY_SPEED
            self.collisions('vertical')

        
    

    def collisions(self,direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self):
                if direction == 'horizontal':
                    if self.direction.x >0: self.rect.right = sprite.rect.left
                    if self.direction.x<0: self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y >0: self.rect.bottom = sprite.rect.top
                    if self.direction.y <0: self.rect.top = sprite.rect.bottom

    def animation(self,dt):

        if self.direction.x<=0:
            self.folder = 'guard right'

        if self.direction.x>0:
            self.folder = 'guard left'
        

        self.frame_index += dt*5
        self.image = pygame.image.load(join('images', 'Guard', self.folder,f'{int(self.frame_index%4)}.png'))
        self.rect = self.image.get_frect(center = self.rect.center)
        
        


    def update(self,dt):
        self.move(dt)
        self.animation(dt)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()
        self.half_w = WIN_WIDTH//2
        self.half_h = WIN_HEIGHT//2
        
        # internal surf
        self.internal_surf_size = INT_SURF_SIZE
        self.internal_surf = pygame.Surface(self.internal_surf_size,pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0]//2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1]//2 - self.half_h




        self.zoom_scale = 2.589999999999999


    # def zoom(self):


    def draw(self,target_pos):
        self.offset.x = -(target_pos[0] - WIN_WIDTH/2)
        self.offset.y = -(target_pos[1] - WIN_HEIGHT/2)

        self.internal_surf.fill(BG_COLOR)

        # ground_sprites = [sprite for sprite in self if hasattr(sprite, 'Ground') or hasattr(sprite, 'Decoration')]
        
        # object_sprites = [sprite for sprite in self if not hasattr(sprite, 'Ground')]
        
        

        for sprite in self:
            self.internal_surf.blit(sprite.image, sprite.rect.topleft + self.offset + self.internal_offset)
        

        scaled_surf = pygame.transform.smoothscale(self.internal_surf, self.internal_surface_size_vector*self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))
        self.display_surface.blit(scaled_surf,scaled_rect)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        pygame.display.set_caption('''Vampire's Prision Escape ''')
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True


        # conditions
        self.forest = False
        self.out_of_cell = True
        self.start_game = False
        self.died = False
        self.disp_bet = False
        self.disp_hint = False
        self.show_title_screen = True
        self.bat_hint_displ = False
        self.can_disp_hint = False
        self.became_bat_after_hint = False
        

        # Groups:
        self.all_sprites = CameraGroup()
        self.collision_sprities = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.chest_sprites = pygame.sprite.Group()
        self.door_sprites1 = pygame.sprite.Group()
        self.Guard1_rect_group = pygame.sprite.Group()
        self.Guard_sprites_group = pygame.sprite.Group()
        self.Blood_throws = pygame.sprite.Group()
        self.Tree_group = pygame.sprite.Group()


        # guard groups
        self.guard_image = pygame.Surface((16,16))

        self.gaurd1_pos = []

        self.map_exit = pygame.sprite.Group()

        # enemy pos
        self.forest_enemy_pos = []

        # timers
        self.enemy_event = pygame.event.custom_type()
        self.enemy_timer = pygame.time.set_timer(self.enemy_event,DINO_ENEMY_SPAWN_RATE)

        self.dungeon_enemy_event = pygame.event.custom_type()
        self.dungeon_enemy_event_timer = pygame.time.set_timer(self.dungeon_enemy_event,DUN_ENEMY_SPAWN_RATE)

        self.hint_event = pygame.event.custom_type()
        self.hint_timer = pygame.time.set_timer(self.hint_event,7000)




        self.bloodthrow_prev =0


        # highscore
        
        try:
            with open(join('Data', 'highsore.txt')) as score_file:
                self.high_score = json.load(score_file)
        except:
            self.high_score = 0

        

        # Dungeon:
        self.key =0;
        
        # indexs
            # instruction start game
        self.instruction_index = 0
            # end_sceen
        self.end_screen_index =0
        self.instruction_shown = False
        self.escaped_time = 0
        self.end_screen_text= ['''Whew!''', '''That was close''']
        self.end_game = False
            # 
        self.bet_index =0
        

        # load map
        
        self.title_screen()
        
    def collideTree(self):
        for sprite in self.Tree_group:
            if pygame.sprite.collide_rect(self.player,sprite):
                self.player.health += 5
                self.player.health = min(PLAYER_HEALTH,self.player.health)

    def display_key(self):
        key_font = pygame.font.Font(key_font_type,key_font_size)
        key_font_surf = key_font.render(f'Keys: {self.key}',False,Key_font_collor)
        key_rect = key_font_surf.get_rect(topleft = key_disp_place)
        self.screen.blit(key_font_surf,key_rect)
        
    def chest_colision(self):
        collision = pygame.sprite.spritecollide(self.player, self.chest_sprites, True, pygame.sprite.collide_mask)
        if collision:
            for sprite in collision:
                self.collision_sprities.remove(sprite)
                self.all_sprites.remove(sprite)
            
            return True
        return False

    def End_screen(self):
        self.high_score = min(self.escaped_time,self.high_score)
        with open(join('data', 'highsore.txt'),'w') as score_file:
            json.dump(self.high_score,score_file)


        end_screen_font =  pygame.font.Font(END_SCREEN_FONT,END_FONT_SIZE)
        # self.screen.fill(END_SCREEN_BG_COLOR)
        bg_scaled = pygame.transform.scale(END_SCREEN_BG,(WIN_WIDTH,WIN_HEIGHT))
        bg_rect = bg_scaled.get_frect(center = (WIN_WIDTH/2,WIN_HEIGHT/2))
        self.screen.blit(bg_scaled,bg_rect)

        end_screen_instruc = end_screen_font.render('press space to continue',True,END_SCREEN_COLOR)
        
        self.screen.blit(end_screen_instruc,(WIN_WIDTH/2-100,WIN_HEIGHT/2+50))

        
        keys = pygame.key.get_just_pressed()

        
        
        if self.end_screen_index < len(self.end_screen_text):
            end_screen_surf = end_screen_font.render(self.end_screen_text[self.end_screen_index],True,END_SCREEN_COLOR)

            if self.end_screen_index < 2:
                self.screen.blit(end_screen_surf, END_FONT_POOS)
            if self.end_screen_index ==2:
                self.screen.blit(end_screen_surf,(WIN_WIDTH/2-450,WIN_HEIGHT/2-150))


            if keys[pygame.K_SPACE]:
                self.end_screen_index +=1
                
    def door1_collilde(self):
        if self.player.rect.colliderect(self.EP1R):
            self.collision_sprities.remove(self.door)        
            self.key = self.key-1
            self.out_of_cell = True

    def door2_collilde(self):
        if self.player.rect.colliderect(self.EP2R) and self.key ==1:
            self.collision_sprities.remove(self.door2)        
            self.key = self.key-1
            self.disp_hint = True

        if self.player.rect.colliderect(self.EP2R) and self.key < 1 and self.disp_hint == False:
            hint_font = pygame.font.Font(instruc_font,instruc_font_size)
            hint_surf = hint_font.render('To open this door Get a key,\nfrom a chest!',True, instru_font_color)
            hint_rect = hint_surf.get_frect(topleft = (WIN_WIDTH/2,WIN_HEIGHT/2-100))
            

            self.screen.blit(hint_surf,hint_rect)

    def load_dungeon(self):
        dungeon_map = load_pygame(join('Data', 'Dungeon map','Dungeon Tiles', 'Dungeon_map.tmx'))

        for x,y,image in dungeon_map.get_layer_by_name('Ground').tiles():
            
            Sprite((x*DUN_TILE_SIZE,y*DUN_TILE_SIZE),image,self.all_sprites)

        for x,y,image in dungeon_map.get_layer_by_name('Rooms').tiles():
            Sprite((x*DUN_TILE_SIZE,y*DUN_TILE_SIZE),image,(self.all_sprites,self.collision_sprities))

        for obj in dungeon_map.get_layer_by_name('Entities'):
            if obj.name == 'Map exit':
                Sprite((obj.x,obj.y),obj.image,(self.all_sprites,self.map_exit))

            if obj.name == 'Map exit rect':
                self.MER = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
            
            if obj.name == 'Exit point1 rect':
                self.EP1R = pygame.Rect(obj.x,obj.y,obj.width,obj.height)

            if obj.name == 'Exit point2 rect':
                self.EP2R = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                
            
            if obj.name == 'Exit point1':
                self.door = DoorSprite((obj.x,obj.y),obj.image,(self.all_sprites,self.door_sprites1,self.collision_sprities))

            if obj.name == 'Exit point2':
                self.door2 = DoorSprite((obj.x,obj.y),obj.image,(self.all_sprites,self.door_sprites1,self.collision_sprities))
                
            if obj.name == 'interact':
                self.chest = ChestSprite((obj.x,obj.y),obj.image,(self.all_sprites,self.chest_sprites))
                
            if obj.name == 'Player':
                self.player = PlayerSprite((obj.x,obj.y),self.all_sprites,self.collision_sprities,self.enemies_sprites,self.forest)

            if obj.name == 'RECTGuard':
                Grect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                Gsprite = pygame.sprite.Sprite()
                Gsprite.rect = Grect
                self.Guard1_rect_group.add(Gsprite)

            if obj.name == 'Guards':
                self.gaurd1_pos.append((obj.x,obj.y))
                
            if obj.name == 'Rectangle':
                Sprite((obj.x,obj.y),pygame.Surface((obj.width,obj.height)),self.collision_sprities)
                
        for x,y,image in dungeon_map.get_layer_by_name('Maze walls').tiles():
            Sprite((x*DUN_TILE_SIZE,y*DUN_TILE_SIZE),image,(self.all_sprites,self.collision_sprities))

        for x,y,image in dungeon_map.get_layer_by_name('Decoration').tiles():
            Sprite((x*DUN_TILE_SIZE,y*DUN_TILE_SIZE),image,self.all_sprites)

    def instruction(self):
        key = pygame.key.get_just_pressed()


        instruction_font = pygame.font.Font(instruc_font,instruc_font_size)
        
        if self.forest == False:
            instructions_dun = ['To move press WASD or RGHT-LEFT-UP-DOWN Arrow keys\nPress space to continue', 'To punch press E or Left mouse button\nNOTE: The guards will damage you till their last breath!!\nPress space to continue', 'To Use blood power press Q or right arrow key\nNOTE: The blood throw will go in the direction you are facing\nPress space to continue', 'Collect keys from chests to open doors\nPress space to continue', 'Press T to become a Bat\nNOTE: you can be bat every 3 seconds\nEnemies cant follow you when you are a bat\nPress space to continue' ,'There is a BLACK exit at the other side of the prison,reach it and\nYou will be rescued by GOOSE\nPress space to continue']
            
            if(self.instruction_index < len(instructions_dun)):
                instruction_surf = instruction_font.render(instructions_dun[self.instruction_index],True,instru_font_color,instru_bg_color)
                instru_rect = instruction_surf.get_frect(topleft = instru_pos)
                instru_rect.inflate(2,2)
                self.screen.blit(instruction_surf,instru_rect)

        if self.forest == True:
            instruction_forest = ['Move under a tree QUICK!!!\n\n\nPress space to continue', 'Stupid Goose,\nYou are in the Sun right now\nStay near a tree to shield yourself from the sun\nStay alive till Goose fixes the machine and brings you HOME']
            if self.instruction_index < len(instruction_forest):
                instruction_surf = instruction_font.render(instruction_forest[self.instruction_index],True,forest_instru_color)
                self.screen.blit(instruction_surf,instru_pos)

        if key[pygame.K_SPACE]:
            self.instruction_index+=1

    def load_forest(self):
        
        map = load_pygame(join('Data' , 'Forest map' , 'Forest map.tmx'))

        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite((x*FOREST_TILE_SIZEE,y*FOREST_TILE_SIZEE),image,self.all_sprites)
        
        
        
        for x,y,image in map.get_layer_by_name('Decoration').tiles():
            Sprite((x*FOREST_TILE_SIZEE,y*FOREST_TILE_SIZEE),image,self.all_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = PlayerSprite((obj.x,obj.y),(self.all_sprites),self.collision_sprities,self.enemies_sprites,self.forest)

            if obj.name == 'Trex':
                self.forest_enemy_pos.append((obj.x,obj.y))

            if obj.name == 'Heal':
                tree = pygame.sprite.Sprite()
                tree.rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                self.Tree_group.add(tree)
        
        for obj in map.get_layer_by_name('Trees'):
            TreeSprite((obj.x,obj.y),obj.image,(self.all_sprites))

        for x,y,image in map.get_layer_by_name('Cliff').tiles():
            Sprite((x*FOREST_TILE_SIZEE,y*FOREST_TILE_SIZEE),image,(self.all_sprites,self.collision_sprities))

        for obj in map.get_layer_by_name('Boundary'):
            if obj.name == 'Boundary':
                Sprite((obj.x,obj.y),pygame.Surface((obj.width,obj.height)),self.collision_sprities)

    def spawn_Guards(self):
        for sprite in self.Guard1_rect_group:
            if sprite.rect.colliderect(self.player.rect):
                for pos in self.gaurd1_pos:
                    if sprite.rect.collidepoint(pos) and self.dungeon_enemy_event and self.out_of_cell == True:
                        GuardSprite(pos,self.guard_image,(self.all_sprites,self.enemies_sprites,self.Guard_sprites_group),self.player,self.collision_sprities)

            if not sprite.rect.colliderect(self.player.rect):
                if self.enemies_sprites:
                    for guard in self.Guard_sprites_group:
                        if sprite.rect.colliderect(guard.rect):
                            self.enemies_sprites.remove(guard)
                            guard.kill()
                            
    def blood_throw(self):
        key = pygame.key.get_pressed()
        button = pygame.mouse.get_pressed()

        if (key[pygame.K_q] or button[2]) and ( (pygame.time.get_ticks() - self.bloodthrow_prev) >= PLAYER_BLOOD_COOLDDOWN) and self.player.is_bat == False:
            pos = self.player.rect.center
            self.bloodthrow_prev = pygame.time.get_ticks()
            blood_throw_sound = pygame.mixer.Sound(join('sound', 'blood throw.mp3'))
            blood_throw_sound.play()
            BloodThrow(pos,(self.Blood_throws,self.all_sprites),self.player)

    def blood_enemy_collision(self):
        for sprite in self.Blood_throws:
            collide_with_map = pygame.sprite.spritecollide(sprite,self.collision_sprities,False)
            if collide_with_map:
                sprite.kill()

            

        for sprite in self.Blood_throws:
            enemies_hit =  pygame.sprite.spritecollide(sprite,self.enemies_sprites,True)
            if enemies_hit:
                sprite.kill()
                for enemy in enemies_hit:
                    enemy.health -= BLOOD_THROW_DAMAGE
                    if self.forest == True:
                        dino_death = pygame.mixer.Sound(join('sound', 'dino died sound.mp3'))
                        dino_death.play()
                    if self.forest == False:
                        DUN = pygame.mixer.Sound(join('sound' , 'dun death.mp3'))
                        DUN.play()

    def title_screen(self):
        titel_screen_display_image = pygame.image.load(join('Data' , 'title screen' , 'new title.png'))
        scaled_title_display_image = pygame.transform.scale(titel_screen_display_image,(WIN_WIDTH,WIN_HEIGHT))
        scaled_image_size = scaled_title_display_image.get_size()
        title_screen_rect = scaled_title_display_image.get_frect(center = TITLE_SCREEN_pos)



        txt_pos = (scaled_image_size[0]//2,scaled_image_size[1]//2)
        

        keys = pygame.mouse.get_pressed()

        title_screen_font = pygame.font.Font(TITLE_SCREEN_FONT,TITLE_SCREEN_FONT_SIZE)

        info_font = pygame.font.Font(TITLE_SCREEN_FONT,TITLE_SCREEN_FONT_SIZE - 40)


        title_screen_text = title_screen_font.render('''Vampire's Prison Escape''',True,TITLE_COLOR)
        titeld_screen_text_rect = title_screen_text.get_frect(center = (txt_pos[0], txt_pos[1]))
        
        highcore_surf = info_font.render(f'''Highscore : {self.high_score}''',True, PLAY_COLOR)
        highscore_rect = highcore_surf.get_frect(center = (txt_pos[0],txt_pos[1] - 100))

        title_screen_play = title_screen_font.render('''Play''',True,PLAY_COLOR)
        title_screen_play_rect = title_screen_play.get_frect(center = (txt_pos[0], txt_pos[1]+100))
        self.game_start_at = pygame.time.get_ticks()

        self.screen.blit(scaled_title_display_image,title_screen_rect)
        self.screen.blit(title_screen_text,titeld_screen_text_rect)
        self.screen.blit(title_screen_play,title_screen_play_rect)
        self.screen.blit(highcore_surf,highscore_rect)

        
        if keys[0] and title_screen_play_rect.collidepoint(pygame.mouse.get_pos()):
            
            
            self.game_music = pygame.mixer.Sound(join('sound' , 'game music.mp3'))
            self.game_music.set_volume(0.5)
            self.game_music.play(loops = -1)
            
            self.show_title_screen =False
            self.game_story()

    def Death_screen(self):
        Death_font = pygame.font.Font(DEATH_FONT,DEATH_FONT_SIZE)

        death_text = Death_font.render('You DIED',True,DEATH_FONT_COLOR)
        death_rect = death_text.get_frect(center = DEATH_FONT_POS)

        self.screen.blit(death_text,death_rect)

        keys = pygame.mouse.get_pressed()

        restart_text = 'Restart'
        restart_font = pygame.font.Font(TITLE_SCREEN_FONT,TITLE_SCREEN_FONT_SIZE)
        restart_text_surf = restart_font.render(restart_text,True,TITLE_COLOR)
        restart_rect = restart_text_surf.get_frect(center = (DEATH_FONT_POS[0],DEATH_FONT_POS[1]+200))

        self.screen.blit(restart_text_surf,restart_rect)

        if keys[0] and restart_rect.collidepoint(pygame.mouse.get_pos()):
            self.running =False
            self.all_sprites.empty()
            self.collision_sprities.empty()
            self.enemies_sprites.empty()
            self.chest_sprites.empty()
            self.door_sprites1.empty()
            self.Guard1_rect_group.empty()
            self.Guard_sprites_group.empty()
            self.Blood_throws.empty()
            self.Tree_group.empty()
            self.game_music.stop()
            self.__init__()

    def screen_bet_DUN_and_FOREST(self):
        text = [ '''What's happening?''' , '''Oh no... ''' , '''Remeber Goose? ''' , '''The chicken you hipnotised to make machines for Transalvaniya?''', '''Yeah, looks like he messed up''' , '''You are now being transported to- ''', '''A VERY VERY FAR PAST '''   ]

        sclaed_bet_image = pygame.transform.scale(BET_IMAGE,(WIN_WIDTH,WIN_HEIGHT))
        sclaed_image_size = sclaed_bet_image.get_size()
        
        txt_pos = (sclaed_image_size[0]/2 , sclaed_image_size[1]/2 )
        scaled_image_rect = sclaed_bet_image.get_frect(center = txt_pos)

        self.screen.blit(sclaed_bet_image,scaled_image_rect)

        text_font = pygame.font.Font(BET_SCREEN_FONT_FILE, BET_FONT_SIZE)


        
        

        intruc = text_font.render('''Press Space to Continue''',True,BET_FONT_COLOR)
        intruc_rect = intruc.get_frect(center = (txt_pos[0]/2 , 2*txt_pos[1] - 150))
        self.screen.blit(intruc,intruc_rect)


        keys = pygame.key.get_just_pressed()

        if self.bet_index < len(text):
            text_surf= text_font.render(text[self.bet_index], True, BET_FONT_COLOR)
            text_rect = text_surf.get_frect(center = txt_pos)
            self.screen.blit(text_surf,text_rect)

            if keys[pygame.K_SPACE]:
                self.bet_index +=1

        else: 
            self.disp_bet = False
            self.forest = True
            self.forest_end_event = pygame.event.custom_type()
            self.forest_timer = pygame.time.set_timer(self.forest_end_event,TIME_IN_FOREST)
            self.bat_hint_displ = False
            self.became_bat_after_hint = False
            self.load_forest()

    def game_story(self):
        bg_imgae = pygame.image.load(join('images' , 'Backgrounds' , 'scroll.jpg'))
        scaled_bg_image = pygame.transform.scale(bg_imgae, (WIN_WIDTH,WIN_HEIGHT))
        bg_rect = scaled_bg_image.get_frect(center = (WIN_WIDTH/2,WIN_HEIGHT/2))

        self.screen.blit(scaled_bg_image,bg_rect)




        story = ['''It's the year 1850,\nYou have been caught by humans and have been put in a prision in a dungeon,\nLuckly with your powers and Goose's time-space travelling machine\nAll you need to do is escape through the prison gates from where Goose,\nwill transport you to transylvania\nGood luck VAMP! ''']
        story_font = pygame.font.Font(STORY_FONT,STORY_FONT_SIZE)
        story_surf = story_font.render(story[0],True,STORY_FONT_COLOR)

        story_rect =story_surf.get_frect(center = (WIN_WIDTH/2,WIN_HEIGHT/2))

        # self.screen.fill('black')
        
        self.screen.blit(story_surf,story_rect)


        intru = 'CONTINUE'
        inst_surf = story_font.render(intru,True,'#fc0335')
        inst_rect = inst_surf.get_frect(bottomright = (1100,500))
        self.screen.blit(inst_surf,inst_rect)

        button = pygame.mouse.get_pressed()

        if inst_rect.collidepoint(pygame.mouse.get_pos()) and button[0]:
            self.start_game  = True
            self.load_dungeon()



    async def run(self):
        while self.running:
            # dt
            dt = self.clock.tick()/1000

            # event 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == self.enemy_event and self.forest == True and self.end_game == False:
                    DinoSprite((self.all_sprites,self.enemies_sprites),self.forest_enemy_pos,self.player,self.collision_sprities)
                    

                if event.type == self.dungeon_enemy_event and self.forest == False and self.end_game == False and self.start_game == True:
                    self.spawn_Guards()

                if event.type == pygame.MOUSEWHEEL:
                    self.all_sprites.zoom_scale += event.y*0.03
                    

                if self.forest == True and event.type == self.forest_end_event and self.end_game == False:
                    self.escaped_time += pygame.time.get_ticks() - self.start_game
                    self.end_screen_text.append(f'''With Goose's mishap, You escaped prision in: {self.escaped_time/1000} seconds''')
                    self.end_game = True

                if self.start_game == True and self.player.health <=0:
                    self.died = True

                if self.hint_event:
                        self.can_disp_hint = True
                    


            if self.start_game == True and self.died == False:   
                if self.end_game == False:
                    # change map: / dungeon disp
                    if self.forest == False and self.disp_bet == False:
                        if  self.MER.colliderect(self.player):
                            
                            
                            self.enemies_sprites.empty()
                            self.all_sprites.empty()
                            self.collision_sprities.empty() 
                            self.enemies_sprites.empty()
                            self.chest_sprites.empty()
                            self.door_sprites1.empty()
                            self.Guard1_rect_group.empty()
                            self.Blood_throws.empty()
                            self.instruction_index =0

                            
                            
                            self.screen_bet_DUN_and_FOREST()
                            self.disp_bet = True
                            


                        if self.chest_colision():
                            self.key += 1
                            

                        # see key_updation
                        if self.key==1:
                            self.door1_collilde()
                            
                    if self.forest == True:
                        self.collideTree()
                        self.player.health -= 0.55

                    

                    # update
                    self.all_sprites.update(dt)
                    self.blood_enemy_collision()

                    # draw  
                    
                    self.screen.fill(BG_COLOR)
                    self.all_sprites.draw(self.player.rect.center)
                    self.player.health_bar(self.screen)
                    self.blood_throw()
                    

                    if self.forest == False and self.disp_bet == False:
                        self.display_key()
                        self.door2_collilde()
                        
                    
                    if self.disp_bet == True:
                        self.screen_bet_DUN_and_FOREST()

                    if self.disp_bet == False:
                        self.instruction()

                    if self.can_disp_hint == True and self.player.health < (PLAYER_HEALTH/2 + 10) and self.disp_bet == False and self.became_bat_after_hint == False:
                        hint_font = pygame.font.Font(instruc_font,instruc_font_size)
                        hint_surf = hint_font.render('''If you are overwhelmed with Enemies,\nPress T to become a BAT\nEnemies WON'T attack you when you are a bat and,\nyou can punch (E) your way out''',True,PLAYER_HEALTH_COLOR)
                        hint_rect = hint_surf.get_frect(topleft = (WIN_WIDTH/2-500,(WIN_HEIGHT/2 + 100)))
                        self.screen.blit(hint_surf,hint_rect)

                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_t]:
                            self.became_bat_after_hint = True
                        

                        

                if self.end_game == True:
                    self.End_screen()
                    
                        
                        
                    keys = pygame.key.get_just_pressed()
                    if keys[pygame.K_SPACE] and self.end_screen_index >= len(self.end_screen_text):
                        self.running =False
                        self.all_sprites.empty()
                        self.collision_sprities.empty()
                        self.enemies_sprites.empty()
                        self.chest_sprites.empty()
                        self.door_sprites1.empty()
                        self.Guard1_rect_group.empty()
                        self.Guard_sprites_group.empty()
                        self.Blood_throws.empty()
                        self.Tree_group.empty()
                        self.game_music.stop()
                        self.__init__()
                        

            if self.start_game == False and self.died == False and self.show_title_screen == True:
                self.title_screen()

            if self.start_game == False and self.died == False and self.show_title_screen == False:
                self.game_story()

            if self.died == True:
                self.Death_screen()

            
            pygame.display.update() 

            await asyncio.sleep(0)



        


if __name__ == '__main__':
    game = Game()
    asyncio.run(game.run())
    