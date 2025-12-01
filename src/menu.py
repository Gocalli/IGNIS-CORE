import pygame
import sys
from .settings import *

class Button:
    def __init__(self, text, pos, width, height, font):
        self.original_rect = pygame.Rect(pos, (width, height))
        self.rect = self.original_rect.copy()
        self.text = text
        self.font = font
        self.pos = pos
        self.is_hovered = False

    def draw(self, surface):
        # Color cambia si el mouse está encima
        color = COLOR_PLAYER if self.is_hovered else COLOR_PLATFORM
        text_color = (0, 0, 0) if self.is_hovered else COLOR_TEXT
        
        # Dibujar fondo del botón
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2, border_radius=5)

        # Texto centrado
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.get_surface()
        self.font_title = pygame.font.SysFont('impact', 80)
        self.font_button = pygame.font.SysFont('monospace', 30)
        self.font_text = pygame.font.SysFont('monospace', 20)
        
        # Configurar botones
        center_x = SCREEN_WIDTH // 2 - 100
        start_y = 250
        gap = 70
        
        self.buttons = [
            Button("JUGAR", (center_x, start_y), 200, 50, self.font_button),
            Button("AYUDA", (center_x, start_y + gap), 200, 50, self.font_button),
            Button("CREDITOS", (center_x, start_y + gap * 2), 200, 50, self.font_button),
            Button("SALIR", (center_x, start_y + gap * 3), 200, 50, self.font_button)
        ]
        
        # Estado interno del menú (Main, Help, Credits)
        self.sub_menu = 'main' 

        # Cargar y escalar la imagen de fondo
        self.background_image = pygame.image.load('assets/graphics/menu.jpg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Cargar y escalar la imagen de fondo para la sección de Ayuda
        self.help_image = pygame.image.load('assets/graphics/help.jpg').convert()
        self.help_image = pygame.transform.scale(self.help_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Cargar y escalar la imagen de fondo para la sección de Créditos
        self.credits_image = pygame.image.load('assets/graphics/credits.jpg').convert()
        self.credits_image = pygame.transform.scale(self.credits_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw_main(self):
        # Dibujar la imagen de fondo primero
        self.screen.blit(self.background_image, (0, 0))
        
        # Botones
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.check_hover(mouse_pos)
            btn.draw(self.screen)

    def draw_help(self):
        # Dibujar la imagen de fondo para ayuda
        self.screen.blit(self.help_image, (0, 0))

    def draw_credits(self):
        # Dibujar la imagen de fondo para créditos
        self.screen.blit(self.credits_image, (0, 0))

    def update(self):
        # Dibujar según el sub-menú
        if self.sub_menu == 'main':
            self.draw_main()
        elif self.sub_menu == 'help':
            self.draw_help()
        elif self.sub_menu == 'credits':
            self.draw_credits()
            
        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.sub_menu == 'main':
                    mouse_pos = pygame.mouse.get_pos()
                    for btn in self.buttons:
                        if btn.check_hover(mouse_pos):
                            if btn.text == "JUGAR":
                                self.game.state = 'level' # Cambiar estado en Game
                            elif btn.text == "AYUDA":
                                self.sub_menu = 'help'
                            elif btn.text == "CREDITOS":
                                self.sub_menu = 'credits'
                            elif btn.text == "SALIR":
                                pygame.quit()
                                sys.exit()
                                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.sub_menu != 'main':
                        self.sub_menu = 'main'

class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.get_surface()
        self.font_title = pygame.font.SysFont('impact', 60)
        self.font_button = pygame.font.SysFont('monospace', 30)
        
        center_x = SCREEN_WIDTH // 2 - 125
        center_y = SCREEN_HEIGHT // 2 - 50
        
        self.buttons = [
            Button("CONTINUAR", (center_x, center_y), 250, 50, self.font_button),
            Button("MENU PRINCIPAL", (center_x, center_y + 70), 250, 50, self.font_button)
        ]
        
        # Overlay semitransparente
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(150)

    def draw(self):
        # Dibujar overlay
        self.screen.blit(self.overlay, (0, 0))
        
        # Título PAUSA
        title_surf = self.font_title.render("PAUSA", True, COLOR_TEXT)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        self.screen.blit(title_surf, title_rect)
        
        # Botones
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.check_hover(mouse_pos)
            btn.draw(self.screen)

    def update(self):
        self.draw()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for btn in self.buttons:
                    if btn.check_hover(mouse_pos):
                        if btn.text == "CONTINUAR":
                            self.game.state = 'level'
                        elif btn.text == "MENU PRINCIPAL":
                            self.game.state = 'menu'
                            # Importamos Level aquí para evitar import circular si fuera necesario, 
                            # pero como 'game' ya tiene Level importado, mejor confiamos en game.py para reiniciar
                            # Sin embargo, para simplificar, le pediremos a Game que reinicie el nivel
                            self.game.reset_level() 
                            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.state = 'level'
