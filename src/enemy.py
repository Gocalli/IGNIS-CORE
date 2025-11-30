import pygame
from .settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, distance):
        super().__init__()
        # Cargar imagen
        self.image = pygame.image.load('assets/graphics/enemy/drone.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        
        # Lógica
        self.start_x = pos[0]
        self.max_distance = distance
        self.speed = ENEMY_SPEED
        self.direction = 1 

    def move(self):
        self.rect.x += self.speed * self.direction
        
        if abs(self.rect.x - self.start_x) > self.max_distance:
            self.direction *= -1
            
        # Voltear sprite
        if self.direction > 0:
            self.image = pygame.image.load('assets/graphics/enemy/drone.png').convert_alpha()
        else:
            self.image = pygame.transform.flip(pygame.image.load('assets/graphics/enemy/drone.png').convert_alpha(), True, False)

    def update(self):
        self.move()