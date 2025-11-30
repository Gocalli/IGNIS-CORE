import pygame
from .settings import *

class UI:
    def __init__(self, surface):
        self.display_surface = surface
        self.font = pygame.font.SysFont('monospace', UI_FONT_SIZE) # Fuente estilo terminal

        # Configuración de barras
        self.health_bar_rect = pygame.Rect(10, 10, UI_HEALTH_BAR_WIDTH, UI_BAR_HEIGHT)
        self.heat_bar_rect = pygame.Rect(10, 40, UI_HEAT_BAR_WIDTH, UI_BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        # Fondo de la barra
        pygame.draw.rect(self.display_surface, (50, 50, 50), bg_rect)

        # Cálculo del ancho actual
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Dibujo de la barra actual
        pygame.draw.rect(self.display_surface, color, current_rect)
        # Borde
        pygame.draw.rect(self.display_surface, (200, 200, 200), bg_rect, 2)

    def show_text(self):
        # Etiquetas simples
        health_surf = self.font.render("INTEGRIDAD", False, COLOR_TEXT)
        heat_surf = self.font.render("TEMPERATURA", False, COLOR_TEXT)
        
        self.display_surface.blit(health_surf, (UI_HEALTH_BAR_WIDTH + 20, 10))
        self.display_surface.blit(heat_surf, (UI_HEAT_BAR_WIDTH + 20, 40))

    def display(self, player):
        # Barra de Vida
        self.show_bar(player.health, PLAYER_MAX_HEALTH, self.health_bar_rect, (0, 255, 0))
        
        # Barra de Calor (Cambia de color si está cerca del sobrecalentamiento)
        heat_color = COLOR_HEAT_LOW
        if player.heat > PLAYER_MAX_HEAT * 0.8:
            heat_color = COLOR_HEAT_HIGH
            
        self.show_bar(player.heat, PLAYER_MAX_HEAT, self.heat_bar_rect, heat_color)

        self.show_text()
