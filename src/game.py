import pygame
import sys
from .settings import *
from .level import Level
from .menu import Menu, PauseMenu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        # Estados del juego
        self.state = 'menu' # menu, level, paused
        
        # Componentes
        self.level = Level()
        self.menu = Menu(self) 
        self.pause_menu = PauseMenu(self)

    def reset_level(self):
        self.level = Level()

    def run(self):
        while True:
            # Event Loop Global (Para salir en cualquier momento si es necesario)
            # Nota: El menú tiene su propio loop de eventos interno para clicks, 
            # pero el nivel usa pygame.key.get_pressed() en su mayoría.
            # Moveremos el chequeo básico aquí.
            
            if self.state == 'menu':
                self.menu.update()
                
            elif self.state == 'level':
                # Chequeo de pausa/retorno al menú
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = 'paused'

                self.screen.fill(COLOR_BG)
                self.level.run()
                
            elif self.state == 'paused':
                # No limpiamos la pantalla para ver el nivel de fondo
                self.pause_menu.update()

            pygame.display.update()
            self.clock.tick(FPS)