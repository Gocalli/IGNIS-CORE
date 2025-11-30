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

    def draw_main(self):
        self.screen.fill(COLOR_BG)
        
        # Título con sombra
        title_surf = self.font_title.render(TITLE, True, COLOR_PLAYER)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        # Sombra simple
        shadow_surf = self.font_title.render(TITLE, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH // 2 + 4, 150 + 4))
        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(title_surf, title_rect)

        # Botones
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.check_hover(mouse_pos)
            btn.draw(self.screen)

    def draw_help(self):
        self.screen.fill(COLOR_BG)
        lines = [
            "--- CONTROLES ---",
            "",
            "FLECHAS : Moverse",
            "ESPACIO : Saltar",
            "Z       : Atacar (Martillo)",
            "X       : Dash (Impulso)",
            "C       : Ventilar (Enfriar)",
            "",
            "--- MECANICA ---",
            "¡Cuidado con el calor!",
            "Atacar sube tu temperatura.",
            "Si te sobrecalientas, pierdes vida.",
            "",
            "Presiona ESC para volver"
        ]
        
        for i, line in enumerate(lines):
            surf = self.font_button.render(line, True, COLOR_TEXT)
            rect = surf.get_rect(center=(SCREEN_WIDTH//2, 100 + i * 40))
            self.screen.blit(surf, rect)

    def draw_credits(self):
        self.screen.fill(COLOR_BG)
        lines = [
            "--- CREDITOS ---",
            "",
            "Desarrollado por:",
            "Santiago Castano",
            "",
            "Arte & Diseno:",
            "Santiago Castano",
            "",
            "Motor:",
            "Pygame CE",
            "",
            "Presiona ESC para volver"
        ]
        
        for i, line in enumerate(lines):
            color = COLOR_PLAYER if i % 3 == 0 else COLOR_TEXT
            surf = self.font_button.render(line, True, color)
            rect = surf.get_rect(center=(SCREEN_WIDTH//2, 100 + i * 40))
            self.screen.blit(surf, rect)

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
