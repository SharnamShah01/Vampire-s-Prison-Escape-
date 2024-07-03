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
    def __init__(self,pos,groups,collsion_sprtie):
        self.image = pygame.image.load(join('images', 'Vampire', 'Stand', '0.png')).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,Scale_image_by).convert_alpha()
        super().__init__(pos,self.image,groups)
        self.collision_sprite = collsion_sprtie
        self.frames_index = 0
        

        # direction
        self.direction = pygame.Vector2()
        self.speed = PLAYER_SPEED

    def animate(self,dt):
        if self.direction.y >0:
            self.folder = 'down'

        if self.direction.y <0:
            self.folder = 'up'

        if self.direction.x >0:
            self.folder = 'right'

        else:
            self.folder = 'down'
            



        
        self.frames_index += dt*5
        self.image = pygame.image.load(join('images', 'Vampire', self.folder, f'{int(self.frames_index%5)}.png'))
        self.image = pygame.transform.rotozoom(self.image,0,Scale_image_by).convert_alpha()
        self.rect = self.image.get_frect(center = self.rect.center)
            

    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = (int(keys[pygame.K_d]) or int(keys[pygame.K_RIGHT])) - (int(keys[pygame.K_a]) or int(keys[pygame.K_LEFT]))
        self.direction.y = (int(keys[pygame.K_s]) or int(keys[pygame.K_DOWN])) - (int(keys[pygame.K_w]) or int(keys[pygame.K_UP]))

        self.direction = self.direction.normalize() if self.direction else self.direction

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
    def __init__(self,pos,image,groups,player):
        super().__init__(pos,image,groups)
        self.direction = pygame.Vector2()
        self.player = player

    def move(self,dt):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()

        self.rect.x += self.direction.x*dt*DUN_ENEMY_SPEED
        self.rect.y += self.direction.y*dt*DUN_ENEMY_SPEED
    

    def update(self,dt):
        self.move(dt)