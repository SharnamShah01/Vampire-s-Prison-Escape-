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
        if self.chest_sprites:
            for sprite in self.chest_sprites:
                collison = pygame.sprite.spritecollide(self.player,self.chest_sprites,True,pygame.sprite.collide_mask)
                if collison:
                    print('collsion there')
                    return True
        return False
    
    def door_collilde(self):
        for sprite in self.door_sprites:
            collision = pygame.sprite.spritecollide(self.player,self.door_sprites1,True,pygame.sprite.collide_mask)
            if collision and self.key >=1:
                self.key = self.key-1;
                self.door_sprites1.clear()
                self.door_sprites1.empty()
                


    def load_dungeon(self):
        dungeon_map = load_pygame(join('Data', 'Dungeon map','Dungeon Tiles', 'Dungeon_map.tmx'))

        for x,y,image in dungeon_map.get_layer_by_name('Ground').tiles():
            Sprite((x*DUN_TILE_SIZE,y*DUN_TILE_SIZE),image,self.all_sprites)

        for x,y,image in dungeon_map.get_layer_by_name('Rooms').tiles():
            Sprite((x*DUN_TILE_SIZE,y*DUN_TILE_SIZE),image,(self.all_sprites,self.collision_sprities))

        for obj in dungeon_map.get_layer_by_name('Entities'):
            if obj.name == 'Map exit':
                Sprite((obj.x,obj.y),obj.image,(self.all_sprites,self.map_exit))
                

            if obj.name == 'Exit point2':
                self.door = DoorSprite((obj.x,obj.y),obj.image,(self.all_sprites,self.door_sprites1))
                if self.key >= 1:
                    self.door.kill()
                    self.key -= 1

            if obj.name == 'interact':
                self.chest = Sprite((obj.x,obj.y),obj.image,(self.all_sprites,self.collision_sprities,self.chest_sprites))
                

            if obj.name == 'Player':
                self.player = PlayerSprite((obj.x,obj.y),self.all_sprites,self.collision_sprities)

            if obj.name == 'Guards':
                pass

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
                    

            # see key_updation
            if self.chest_colision() == True:
                self.key += 1
                print(self.key)
            # update
            self.all_sprites.update(dt)
            

            # draw
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)


            pygame.display.update() 


        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()