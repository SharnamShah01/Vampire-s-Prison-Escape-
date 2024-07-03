from Settings import *

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
        

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surface_size_vector*self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))
        self.display_surface.blit(scaled_surf,scaled_rect)

        print(self.zoom_scale)

