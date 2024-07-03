from cmath import rect
from tkinter import Frame
from Settings import *
from random import choice

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



class PlayerSprite(Sprite):
    def __init__(self,pos,groups,collsion_sprtie,enemy_sprites):
        self.folder = 'stand down'
        self.image = pygame.image.load(join('images', 'Vampire', self.folder, '0.png')).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image,Scale_image_by).convert_alpha()
        super().__init__(pos,self.image,groups)
        self.enemy_sprite_group = enemy_sprites
        self.collision_sprite = collsion_sprtie
        self.frames_index = 0
        
        # powers
        self.health = PLAYER_HEALTH
        self.damage = PLAYER_DAMAGE

        self.attack = False
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN #can attack once only 500ms
        self.prev_attak =0;


        # direction
        self.direction = pygame.Vector2()
        self.speed = PLAYER_SPEED

        self.prev_dir = pygame.Vector2()

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

        if keys[pygame.K_r] or button[0] and (pygame.time.get_ticks() - self.prev_attak >= self.attack_cooldown):
            self.attack = True
            self.prev_attak = pygame.time.get_ticks()
            print('attakced')
        else: self.attack = False

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

        for sprite in self.enemy_sprite_group:
            if pygame.sprite.collide_mask(self,sprite):
                if self.attack == True:
                    sprite.health -= self.damage
                    if sprite.health <=0:
                        sprite.kill()
                elif pygame.time.get_ticks() - sprite.prev_attack >= sprite.cooldown: 
                    self.health -= sprite.damage
                    sprite.prev_attack = pygame.time.get_ticks()

    def health_bar(self,display_at):
        ratio = self.health/PLAYER_HEALTH
        pygame.draw.rect(display_at, 'red' , (100,50,100,5))
        pygame.draw.rect(display_at, 'green' , (100,50,100*ratio,5))


    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)


class EnemySprite(Sprite):
    def __init__(self,pos,groups,player,collision_sprites):
        self.pos = choice((pos))
        self.image = pygame.Surface((64,64))
        super().__init__(self.pos,self.image,groups)
        self.player = player
        self.collision_sprites = collision_sprites

        self.health = ENEMY_HEALTH
        self.damage = ENEMY_DAMAGE
        self.cooldown = ENEMY_ATTACK_COOLDOWN
        self.prev_attack =0

        # directio
        self.direction = pygame.Vector2()
        self.speed = ENEMY_SPEED



    def get_direction(self,dt):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()


        self.rect.x += self.direction.x*self.speed*dt
        self.collision('horizontal')
        self.rect.y += self.direction.y*self.speed*dt
        self.collision('vertical')


    def collision(self,direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right

                if self.direction == 'vertical':
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    if self.direction.y >0: self.rect.bottom = sprite.rect.top

    def update(self,dt):
        self.get_direction(dt)


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

        if self.direction.x<0:
            self.folder = 'guard right'

        if self.direction.x>0:
            self.folder = 'guard left'
        

        self.frame_index += dt*5
        self.image = pygame.image.load(join('images', 'Guard', self.folder,f'{int(self.frame_index%4)}.png'))
        self.rect = self.image.get_frect(center = self.rect.center)
        print(int(self.frame_index%4))
        


    def update(self,dt):
        self.move(dt)
        self.animation(dt)