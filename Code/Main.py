from Settings import *



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True



    def run(self):
        # event loop
        while self.running:
            # dt
            dt = self.clock.tick()/1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    

            
            # update


            # draw
            self.display_surface.fill('grey')

            pygame.display.update() 


        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()