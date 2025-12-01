import pygame
from .settings import *
from .support import import_spritesheet_row

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, distance):
        super().__init__()
        # Cargar animaciones
        self.frames = import_spritesheet_row('assets/graphics/enemy/idle_drone.png', 189, 94, 4)
        
        # Escalar a tamaño de juego (altura 64px)
        scaled_frames = []
        target_height = 64
        for frame in self.frames:
            scale = target_height / frame.get_height()
            new_width = int(frame.get_width() * scale)
            new_height = int(frame.get_height() * scale)
            scaled_frames.append(pygame.transform.scale(frame, (new_width, new_height)))
        self.frames = scaled_frames

        self.frame_index = 0
        self.animation_speed = 0.15
        
        if self.frames:
            self.image = self.frames[self.frame_index]
        else:
            # Fallback simple si falla la carga
            self.image = pygame.Surface((64, 64))
            self.image.fill('red')
            
        self.rect = self.image.get_rect(topleft=pos)
        
        # Lógica de movimiento
        self.start_x = pos[0]
        self.max_distance = distance
        self.speed = ENEMY_SPEED
        self.direction = 1 

    def animate(self):
        if not self.frames:
            return

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
            
        image = self.frames[int(self.frame_index)]
        
        # Voltear sprite según dirección
        if self.direction > 0:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

    def move(self):
        self.rect.x += self.speed * self.direction
        
        if abs(self.rect.x - self.start_x) > self.max_distance:
            self.direction *= -1

    def update(self):
        self.move()
        self.animate()