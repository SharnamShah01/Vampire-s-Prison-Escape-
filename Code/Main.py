from Settings import *
from Sprites import *
from Groups import *




class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True


        # conditions
        self.forest = False
        self.out_of_cell = True
        self.start_game = False
        self.died = False
        self.disp_bet = False

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

        # enemy spawn timer
        self.enemy_event = pygame.event.custom_type()
        self.enemy_timer = pygame.time.set_timer(self.enemy_event,DINO_ENEMY_SPAWN_RATE)

        self.dungeon_enemy_event = pygame.event.custom_type()
        self.dungeon_enemy_event_timer = pygame.time.set_timer(self.dungeon_enemy_event,DUN_ENEMY_SPAWN_RATE)

        self.bloodthrow_prev =0

        

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
        end_screen_font =  pygame.font.Font(END_SCREEN_FONT,END_FONT_SIZE)
        self.screen.fill(END_SCREEN_BG_COLOR)

        end_screen_instruc = end_screen_font.render('press space to continue',True,END_SCREEN_COLOR)
        
        self.screen.blit(end_screen_instruc,(WIN_WIDTH/2,WIN_HEIGHT-200))

        
        keys = pygame.key.get_just_pressed()

        print(self.end_screen_index)
        
        if self.end_screen_index < len(self.end_screen_text):
            end_screen_surf = end_screen_font.render(self.end_screen_text[self.end_screen_index],True,END_SCREEN_COLOR)

            if self.end_screen_index < 2:
                self.screen.blit(end_screen_surf, END_FONT_POOS)
            if self.end_screen_index ==2:
                self.screen.blit(end_screen_surf, (WIN_WIDTH/2 - 450,WIN_HEIGHT/2))


            if keys[pygame.K_SPACE]:
                self.end_screen_index +=1
                
    def door1_collilde(self):
        if self.player.rect.colliderect(self.EP1R):
            self.collision_sprities.remove(self.door)        
            self.key = self.key-1
            self.out_of_cell = True

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

            if obj.name == 'Map exit rect':
                self.MER = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
            
            if obj.name == 'Exit point1 rect':
                self.EP1R = pygame.Rect(obj.x,obj.y,obj.width,obj.height)

            if obj.name == 'Exit point2 rect':
                self.EP2R = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                print('EP2R MADE')
            
            if obj.name == 'Exit point1':
                self.door = DoorSprite((obj.x,obj.y),obj.image,(self.all_sprites,self.door_sprites1,self.collision_sprities))

            if obj.name == 'Exit point2':
                print('door2 made')
                self.door2 = DoorSprite((obj.x,obj.y),obj.image,(self.all_sprites,self.door_sprites1,self.collision_sprities))
                
            if obj.name == 'interact':
                self.chest = ChestSprite((obj.x,obj.y),obj.image,(self.all_sprites,self.chest_sprites))
                
            if obj.name == 'Player':
                self.player = PlayerSprite((obj.x,obj.y),self.all_sprites,self.collision_sprities,self.enemies_sprites)

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
            instructions_dun = ['To move press WASD or RGHT-LEFT-UP-DOWN Arrow keys\nPress space to continue', 'To punch press E or Left mouse button\nPress space to continue', 'To Use blood power press Q or right arrow key\nPress space to continue', 'Collect keys from chests to open doors\nPress space to continue', 'Press T to become a Bat\nYou can be bat for only 3 Sec Every 3 sec,\nEnemies cant follow you when you are a bat\nPress space to continue' ,'There is a exit at the other side of the prison,reach it and\nYou will be rescued by GOOSE\nPress space to continue']
            
            if(self.instruction_index < len(instructions_dun)):
                instruction_surf = instruction_font.render(instructions_dun[self.instruction_index],True,instru_font_color,instru_bg_color)
                instru_rect = instruction_surf.get_frect(topleft = instru_pos)
                instru_rect.inflate(2,2)
                self.screen.blit(instruction_surf,instru_rect)

        if self.forest == True:
            instruction_forest = ['Move under a tree QUICK!!!', 'Stupid Goose,\nYou are in the Sun right now\nStay near a tree to sheif from the sun\nStay alive till Goose fixes the machine and brings you HOME']
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
                self.player = PlayerSprite((obj.x,obj.y),(self.all_sprites),self.collision_sprities,self.enemies_sprites)

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
                            print('dead')

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

    def title_screen(self):
        titel_screen_display_image = pygame.image.load(join('Data' , 'title screen' , 'new title.png'))
        scaled_title_display_image = pygame.transform.scale(titel_screen_display_image,(WIN_WIDTH,WIN_HEIGHT))
        scaled_image_size = scaled_title_display_image.get_size()
        title_screen_rect = scaled_title_display_image.get_frect(center = TITLE_SCREEN_pos)



        txt_pos = (scaled_image_size[0]//2,scaled_image_size[1]//2)
        

        keys = pygame.mouse.get_pressed()

        title_screen_font = pygame.font.Font(TITLE_SCREEN_FONT,TITLE_SCREEN_FONT_SIZE)


        title_screen_text = title_screen_font.render('''Vampire's Prison Escape''',True,TITLE_COLOR)
        titeld_screen_text_rect = title_screen_text.get_frect(center = (txt_pos[0], txt_pos[1]))
        


        title_screen_play = title_screen_font.render('''Play''',True,PLAY_COLOR)
        title_screen_play_rect = title_screen_play.get_frect(center = (txt_pos[0], txt_pos[1]+100))

        self.screen.blit(scaled_title_display_image,title_screen_rect)
        self.screen.blit(title_screen_text,titeld_screen_text_rect)
        self.screen.blit(title_screen_play,title_screen_play_rect)

        
        if keys[0] and title_screen_play_rect.collidepoint(pygame.mouse.get_pos()):
            
            self.start_game  = True
            self.load_dungeon()

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
            self.load_forest()
            
    def run(self):

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
                    self.escaped_time += pygame.time.get_ticks()
                    self.end_screen_text.append(f'''With Goose's mishap, You escaped prision in: {self.escaped_time/1000} seconds''')
                    self.end_game = True

                if self.start_game == True and self.player.health <=0:
                    self.died = True

                # if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                #     if pygame.mouse.get_pressed()[2] or event.key == pygame.K_q :
                #         self.blood_throw()

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
                            self.door2_collilde()

                    if self.forest == True:
                        self.collideTree()
                        self.player.health -= 1

                    

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
                        
                    
                    if self.disp_bet == True:
                        self.screen_bet_DUN_and_FOREST()

                    if self.disp_bet == False:
                        self.instruction()


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
                        self.__init__()
                        

            if self.start_game == False and self.died == False:
                self.title_screen()

            if self.died == True:
                self.Death_screen()


            pygame.display.update() 

        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()