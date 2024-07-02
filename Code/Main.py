from Settings import *
from Sprites import *
from Groups import *




class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True


        # Groups:
        self.all_sprites = ALLSprites()
        self.collision_sprities = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.chest_sprites = pygame.sprite.Group()
        self.door_sprites1 = pygame.sprite.Group()
        self.Guard1_rect_group = pygame.sprite.Group()

        # guard groups
        self.guard_image = pygame.Surface((16,16))

        self.gaurd1_pos = []

        self.map_exit = pygame.sprite.Group()

        # enemy pos
        self.enemy_pos = []

        # enemy spawn timer
        self.enemy_event = pygame.event.custom_type()
        self.enemy_timer = pygame.time.set_timer(self.enemy_event,ENEMY_SPAWN_RATE)

        

        # Dungeon:
        self.door = []
        self.key =0;
        # load map
        self.load_dungeon()

    
        
    def chest_colision(self):
        collision = pygame.sprite.spritecollide(self.player, self.chest_sprites, True, pygame.sprite.collide_mask)
        if collision:
            for sprite in collision:
                self.collision_sprities.remove(sprite)
                self.all_sprites.remove(sprite)
            
            return True
        return False

    def door1_collilde(self):
        if self.player.rect.colliderect(self.EP1R):
            print('door collide')
            self.collision_sprities.remove(self.door)        
            self.key = self.key-1

    def door2_collilde(self):
        if self.player.rect.colliderect(self.EP2R):
            self.collision_sprities.remove(self.door2)        
            self.key = self.key-1

    def load_dungeon(self):
        dungeon_map = load_pygame(join('Data', 'Dungeon map','Dungeon Tiles', 'Dungeon_map.tmx'))

        for x,y,image in dungeon_map.get_layer_by_name('Ground').tiles():
            Sprite((x*DUN_TILE_SIZE,y*DUN_TILE_SIZE),image,self.all_sprites)

        for x,y,image in dungeon_map.get_layer_by_name('Rooms').tiles():
            Sprite((x*DUN_TILE_SIZE,y*DUN_TILE_SIZE),image,(self.all_sprites,self.collision_sprities))

        for obj in dungeon_map.get_layer_by_name('Entities'):
            if obj.name == 'Map exit':
                Sprite((obj.x,obj.y),obj.image,(self.all_sprites,self.map_exit))
            
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
                self.player = PlayerSprite((obj.x,obj.y),self.all_sprites,self.collision_sprities)

            if obj.name == 'Guards':
                GuardSprite((obj.x,obj.y),self.guard_image,(self.all_sprites))

            if obj.name == 'RECTGuard1':
                Grect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                Gsprite = pygame.sprite.Sprite()
                Gsprite.rect = Grect
                self.Guard1_rect_group.add(Gsprite)

            if obj.name == 'Guards1':
                self.gaurd1_pos.append((obj.x,obj.y))
                
            if obj.name == 'Rectangle':
                Sprite((obj.x,obj.y),pygame.Surface((obj.width,obj.height)),self.collision_sprities)
                
        for x,y,image in dungeon_map.get_layer_by_name('Maze walls').tiles():
            Sprite((x*DUN_TILE_SIZE,y*DUN_TILE_SIZE),image,(self.all_sprites,self.collision_sprities))

        for x,y,image in dungeon_map.get_layer_by_name('Decoration').tiles():
            Sprite((x*DUN_TILE_SIZE,y*DUN_TILE_SIZE),image,self.all_sprites)

    def load_map(self):
        map = load_pygame(join('Data','Game map','Game map.tmx'))

        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image,self.all_sprites)

        for x,y,image in map.get_layer_by_name('Decoration').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image,(self.all_sprites,self.collision_sprities))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = PlayerSprite((obj.x,obj.y),self.all_sprites,self.collision_sprities)
            else:
                self.enemy_pos.append((obj.x,obj.y))

        for obj in map.get_layer_by_name('Trees'):
            TREESprtite((self.all_sprites,self.collision_sprities),(obj.x,obj.y),obj.image)

        for obj in map.get_layer_by_name('World boundary'):
            Sprite((obj.x,obj.y),pygame.Surface((obj.width,obj.height)),self.collision_sprities)

    def spawn_Guards(self):
        for sprite in self.Guard1_rect_group:
            if sprite.rect.colliderect(self.player.rect):
                GuardSprite(self.gaurd1_pos[0],self.guard_image,(self.all_sprites))


    def run(self):
        
        while self.running:
            # dt
            dt = self.clock.tick()/1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # if event.type == self.enemy_event:
                #     EnemySprite(self.enemy_pos,(self.enemies_sprites,self.all_sprites),self.player,self.collision_sprities)
                    

            


            # update
            self.all_sprites.update(dt)
            self.spawn_Guards()

            # see key_updation
            
            if self.chest_colision():
            
                self.key += 1
                print(self.key)

            if self.key==1:
                self.door1_collilde()
                self.door2_collilde()
            
            

            # draw
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)


            pygame.display.update() 


        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()