import pygame
from .settings import *
from .support import import_spritesheet_row

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, distance):
        super().__init__()
        self.import_graphics()
        self.frame_index = 0
        self.animation_speed = 0.12
        self.status = 'move'
        
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        
        # Movimiento
        self.start_x = pos[0]
        self.max_distance = distance
        self.speed = ENEMY_SPEED
        self.direction = 1 
        
        # Combate
        self.health = 3
        self.can_attack = True
        self.attack_time = 0
        self.attack_cooldown = ENEMY_ATTACK_COOLDOWN

    def import_graphics(self):
        self.animations = {'move': [], 'attack': [], 'die': []}
        target_height = 64

        # --- IDLE / MOVE (idle_drone.png) ---
        # Usamos el idle como animación de movimiento por ahora
        idle_frames = import_spritesheet_row('assets/graphics/enemy/idle_drone.png', 189, 94, 4)
        scaled_idle = []
        for frame in idle_frames:
            scale = target_height / frame.get_height()
            new_w = int(frame.get_width() * scale)
            new_h = int(frame.get_height() * scale)
            scaled_idle.append(pygame.transform.scale(frame, (new_w, new_h)))
        self.animations['move'] = scaled_idle

        # --- ATTACK (attack_drone.png) ---
        # Estructura especial: 208, 208, resto. Altura 94.
        try:
            attack_sheet = pygame.image.load('assets/graphics/enemy/attack_drone.png').convert_alpha()
            sheet_w = attack_sheet.get_width()
            sheet_h = attack_sheet.get_height() # Debería ser 94
            
            # Definir recortes
            crops = [
                (0, 0, 208, 94),
                (208, 0, 208, 94),
                (416, 0, sheet_w - 416, 94)
            ]
            
            scaled_attack = []
            for (x, y, w, h) in crops:
                # Crear surface
                frame_surf = pygame.Surface((w, h), pygame.SRCALPHA)
                frame_surf.blit(attack_sheet, (0, 0), pygame.Rect(x, y, w, h))
                
                # Escalar
                scale = target_height / h
                new_w = int(w * scale)
                new_h = int(h * scale)
                scaled_attack.append(pygame.transform.scale(frame_surf, (new_w, new_h)))
            
            self.animations['attack'] = scaled_attack
            
        except Exception as e:
            print(f"Error cargando attack_drone: {e}")
            # Fallback: usar move
            self.animations['attack'] = self.animations['move']

        # --- DIE (die_drone.png) ---
        # 816x136 -> 4 frames de 204x136
        try:
            die_frames = import_spritesheet_row('assets/graphics/enemy/die_drone.png', 204, 136, 4) # Corrected: 4 frames of 204x136
            scaled_die = []
            for frame in die_frames:
                scale = target_height / frame.get_height()
                new_w = int(frame.get_width() * scale)
                new_h = int(frame.get_height() * scale)
                scaled_die.append(pygame.transform.scale(frame, (new_w, new_h)))
            self.animations['die'] = scaled_die
        except Exception as e:
             print(f"Error cargando die_drone: {e}")

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
            
        return (distance, direction)

    def get_status(self, player):
        if self.status == 'die':
            return

        distance, _ = self.get_player_distance_direction(player)
        
        if distance < ENEMY_ATTACK_DISTANCE:
            self.status = 'attack'
        else:
            self.status = 'move'

    def actions(self, player):
        if self.status == 'move':
            self.move()
        elif self.status == 'attack':
            self.attack_logic()
        elif self.status == 'die':
            pass

    def move(self):
        self.rect.x += self.speed * self.direction
        
        if abs(self.rect.x - self.start_x) > self.max_distance:
            self.direction *= -1
            
    def attack_logic(self):
        current_time = pygame.time.get_ticks()
        if self.can_attack:
            # Aquí iniciaría el daño real, por ahora solo animación
            self.can_attack = False
            self.attack_time = current_time
            self.frame_index = 0 # Reiniciar animación al atacar

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    def take_damage(self):
        if self.status == 'die':
            return

        self.health -= 1
        if self.health <= 0:
            self.health = 0
            self.status = 'die'
            self.frame_index = 0

    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'die':
                self.frame_index = len(animation) - 1
            elif self.status == 'attack':
                # Si termina el ataque, esperamos al cooldown
                self.frame_index = 0 
            else:
                self.frame_index = 0
            
        image = animation[int(self.frame_index)]
        
        # Voltear sprite según dirección de movimiento
        if self.direction > 0:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

    def update(self, player):
        self.get_status(player)
        self.actions(player)
        self.cooldowns()
        self.animate()

class Boss(Enemy):
    def __init__(self, pos, distance):
        super().__init__(pos, distance)
        self.health = 50  # Más vida que el enemigo normal
        self.attack_cooldown = 1500
        self.speed = 1.5 # Más lento por ser grande
        
        # Asegurar que use la animación correcta al inicio
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

    def move(self):
        pass

    def import_graphics(self):
        self.animations = {'move': [], 'attack': [], 'die': []}
        target_height = 320  # Boss mucho más grande (Personaje ~64)

        # --- IDLE (Usado para move) ---
        # idle_boss.png: 768x283 -> 3 frames de 256x283
        try:
            idle_frames = import_spritesheet_row('assets/graphics/enemy/idle_boss.png', 256, 283, 3)
            scaled_idle = []
            for frame in idle_frames:
                scale = target_height / frame.get_height()
                new_w = int(frame.get_width() * scale)
                new_h = int(frame.get_height() * scale)
                scaled_idle.append(pygame.transform.scale(frame, (new_w, new_h)))
            self.animations['move'] = scaled_idle
        except Exception as e:
            print(f"Error cargando idle_boss: {e}")

        # --- ATTACK ---
        # attack_boss.png: 998x302. Asumimos 4 frames distribuidos.
        try:
            attack_sheet = pygame.image.load('assets/graphics/enemy/attack_boss.png').convert_alpha()
            sheet_w = attack_sheet.get_width()
            sheet_h = attack_sheet.get_height()
            num_frames = 4
            frame_w = sheet_w // num_frames # ~249

            scaled_attack = []
            for i in range(num_frames):
                x = i * frame_w
                w = frame_w
                
                frame_surf = pygame.Surface((w, sheet_h), pygame.SRCALPHA)
                frame_surf.blit(attack_sheet, (0, 0), pygame.Rect(x, 0, w, sheet_h))
                
                scale = target_height / sheet_h
                new_w = int(w * scale)
                new_h = int(sheet_h * scale)
                scaled_attack.append(pygame.transform.scale(frame_surf, (new_w, new_h)))
            
            self.animations['attack'] = scaled_attack
        except Exception as e:
            print(f"Error cargando attack_boss: {e}")
            self.animations['attack'] = self.animations['move']

        # --- DIE ---
        # Por ahora usamos el idle/move como placeholder si no hay asset de muerte
        self.animations['die'] = self.animations['move']