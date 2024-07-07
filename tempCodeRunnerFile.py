pygame.init()
        pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        pygame.display.set_caption('''Vampire's Prision Escape ''')
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
