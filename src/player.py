import pygame
from .settings import *
from .support import import_folder, import_spritesheet_row

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        
        # Estado de Animación
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'idle'
        self.facing_right = True
        
        # Imagen inicial
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        
        # Movimiento
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.gravity = PLAYER_GRAVITY
        self.jump_force = PLAYER_JUMP_FORCE
        self.on_ground = False
        
        # Stats
        self.health = PLAYER_MAX_HEALTH
        self.heat = 0
        self.overheated = False
        
        # Combate
        self.attacking = False
        self.attack_cooldown = ATTACK_COOLDOWN
        self.attack_time = 0
        self.attack_rect = pygame.Rect(0,0,0,0)

        # Dash
        self.dashing = False
        self.can_dash = True
        self.dash_time = 0
        self.dash_cooldown_time = 0

    def import_character_assets(self):
        path = 'assets/graphics/player/'
        self.animations = {'idle': [], 'run': [], 'run_overheated': [], 'jump': [], 'fall': [], 'attack': []}
        
        # --- IDLE ---
        raw_idle = import_spritesheet_row(path + 'idle_spritesheet.png', 188, 188, 4)
        self.animations['idle'] = [pygame.transform.scale(img, (64, 64)) for img in raw_idle]
        
        # --- RUN (Normal + Overheated) ---
        # 7 frames total: 0-2 normal, 3-6 overheated
        raw_run = import_spritesheet_row(path + 'run_spritesheet.png', 188, 188, 7)
        if raw_run:
            scaled_run = [pygame.transform.scale(img, (64, 64)) for img in raw_run]
            self.animations['run'] = scaled_run[0:3]           # Frames 0, 1, 2
            self.animations['run_overheated'] = scaled_run[3:] # Frames 3, 4, 5, 6
        
        self.player_rect_size = (64, 64) 
        
        # --- JUMP ---
        # 3 frames, 188x234. Escalamos a 64x80 para mantener proporción.
        raw_jump = import_spritesheet_row(path + 'jump_spritesheet.png', 188, 234, 3)
        if raw_jump:
             self.animations['jump'] = [pygame.transform.scale(img, (64, 80)) for img in raw_jump]

        def load_safe(filename):
            try:
                return pygame.image.load(path + filename).convert_alpha()
            except FileNotFoundError:
                return None

        # Cargar otras animaciones con chequeo de errores
        # Jump/Fall (Legacy fallback)
        if not self.animations['jump']:
             img = load_safe('jump_0.png')
             if img: self.animations['jump'].append(img)
        
        img = load_safe('fall_0.png')
        if img: self.animations['fall'].append(img)
        
        # Attack
        for i in range(2): 
            img = load_safe(f'attack_{i}.png')
            if img: self.animations['attack'].append(img)
        
        # Fallbacks
        idle_anim = self.animations.get('idle', [])
        if not idle_anim:
            fallback_surf = pygame.Surface((32, 64))
            fallback_surf.fill((255, 0, 255)) 
            idle_anim = [fallback_surf]
            self.animations['idle'] = idle_anim
            self.player_rect_size = (32, 64)

        for anim_name in self.animations.keys():
            if not self.animations[anim_name]:
                self.animations[anim_name] = idle_anim

    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.attacking = False 
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)
            
        if self.overheated and self.status not in ['run_overheated']:
             self.image.fill((255, 50, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)

        # FIX: Anclar al suelo (midbottom) en lugar del centro
        # Esto evita que el personaje "salte" o se hunda cuando cambia el tamaño de la imagen
        previous_rect = self.rect
        self.rect = self.image.get_rect()
        self.rect.midbottom = previous_rect.midbottom
        
        # Ajustar hitbox de colisión (más estrecho que la imagen para perdonar roces)
        # Mantenemos el ancho lógico de 32px pero respetamos la posición visual
        self.rect.width = 32
        self.rect.centerx = previous_rect.centerx # Mantener centro horizontal

    def get_status(self):
        if self.attacking:
            self.status = 'attack'
        elif self.dashing: 
            self.status = 'run' if not self.overheated else 'run_overheated'
        elif self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1: 
            self.status = 'fall'
        elif self.direction.x != 0:
            if self.overheated:
                self.status = 'run_overheated'
            else:
                self.status = 'run'
        else:
            self.status = 'idle'

    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
            
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            
        if keys[pygame.K_z] and not self.attacking:
            self.attack()
            
        if keys[pygame.K_x] and self.can_dash and not self.dashing:
            self.start_dash()
            
        if keys[pygame.K_c]:
            self.vent_heat()

    def apply_gravity(self):
        if not self.dashing:
            self.direction.y += self.gravity
            self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_force
        self.on_ground = False

    def start_dash(self):
        self.dashing = True
        self.can_dash = False
        self.dash_time = pygame.time.get_ticks()
        self.dash_cooldown_time = pygame.time.get_ticks()
        if self.direction.x == 0:
            self.direction.x = 1 if self.facing_right else -1

    def attack(self):
        self.attacking = True
        self.frame_index = 0 
        self.attack_time = pygame.time.get_ticks()
        
        self.heat += HEAT_INCREASE_PER_HIT
        if self.heat >= PLAYER_MAX_HEAT:
            self.heat = PLAYER_MAX_HEAT
            self.overheated = True
            
        facing = 1 if self.facing_right else -1
        # El hitbox de ataque sigue siendo relativo al tamaño lógico del jugador (32x64)
        self.attack_rect = pygame.Rect(
            self.rect.centerx + (10 * facing), 
            self.rect.y, 
            40, 
            self.rect.height
        )

    def vent_heat(self):
        self.heat -= HEAT_COOLDOWN_RATE * 2
        if self.heat < 0:
            self.heat = 0
        self.overheated = False

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.dashing:
            if current_time - self.dash_time >= PLAYER_DASH_DURATION:
                self.dashing = False
                self.direction.x = 0 

        if not self.can_dash:
            if current_time - self.dash_cooldown_time >= PLAYER_DASH_COOLDOWN:
                self.can_dash = True

    def manage_heat(self):
        if self.overheated:
            self.health -= HEAT_DAMAGE_RATE
        
        if not self.attacking and self.heat > 0:
            self.heat -= 0.05

    def update(self):
        self.get_input()
        self.cooldowns()
        self.manage_heat()
        self.get_status()
        self.animate()
        
        if self.dashing:
            self.rect.x += self.direction.x * PLAYER_DASH_SPEED
