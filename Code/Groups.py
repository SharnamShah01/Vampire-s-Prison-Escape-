from Settings import *

class ALLSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()


    def draw(self,target_pos):
        self.offset.x = -(target_pos[0] - WIN_WIDTH/2)
        self.offset.y = -(target_pos[1] - WIN_HEIGHT/2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'Ground') or hasattr(sprite, 'Decoration')]
        
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'Ground')]
        
        for layer in [ground_sprites,object_sprites]:
            for sprite in layer:#sorted(layer, key = lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

