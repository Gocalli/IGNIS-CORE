import pygame
from .settings import *
from .player import Player
from .enemy import Enemy, Boss
from .ui import UI
from .maps import levels # Importar los mapas

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # Background loading
        try:
            self.bg_surf = pygame.image.load('assets/graphics/main_map.png').convert()
            # ESCALAR: Ajustar la altura a 720 manteniendo aspect ratio
            scale = 720 / self.bg_surf.get_height()
            new_w = int(self.bg_surf.get_width() * scale)
            new_h = 720
            self.bg_surf = pygame.transform.scale(self.bg_surf, (new_w, new_h))
            print(f"Mapa cargado y escalado a: {new_w}x{new_h}")
        except FileNotFoundError:
            print("AVISO: 'assets/graphics/main_map.png' no encontrado. Usando fondo placeholder.")
            self.bg_surf = pygame.Surface((5000, 720)) 
            self.bg_surf.fill((20, 30, 50))
            
        self.bg_rect = self.bg_surf.get_rect(topleft=(0,0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h

        # Dibujar Fondo (Background)
        bg_offset = self.bg_rect.topleft - self.offset
        self.display_surface.blit(self.bg_surf, bg_offset)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            
            if isinstance(sprite, Player) and sprite.attacking:
                 attack_rect_offset = sprite.attack_rect.move(-self.offset.x, -self.offset.y)
                 

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        self.visible_sprites = CameraGroup() 
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        self.ui = UI(self.display_surface)
        
        # Gestión de Niveles
        self.current_level_index = 0
        self.create_map(self.current_level_index)

    def create_map(self, index):
        # Limpiar grupos
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        self.enemy_sprites.empty()
        
        # Cargar mapa según índice
        if index >= len(levels):
            index = 0
            self.current_level_index = 0
            
        layout = levels[index]
        
        # Calcular ancho del nivel para saber cuándo cambiar
        self.level_width = len(layout[0]) * TILE_SIZE

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if cell == 'X':
                    tile = pygame.sprite.Sprite(self.visible_sprites, self.obstacle_sprites)
                    # Usar los tamaños de plataforma configurables
                    tile.image = pygame.Surface((PLATFORM_TILE_WIDTH, PLATFORM_TILE_HEIGHT), pygame.SRCALPHA)

                    tile.rect = tile.image.get_rect(topleft=(x, y))
                
                if cell == 'P':
                    self.player = Player((x, y))
                    self.visible_sprites.add(self.player)
                    
                if cell == 'E':
                    enemy = Enemy((x, y + TILE_SIZE // 2), 200) # Ajuste y + 32 a y + TILE_SIZE // 2
                    self.visible_sprites.add(enemy)
                    self.enemy_sprites.add(enemy)
                
                if cell == 'B':
                    boss = Boss((x, y + TILE_SIZE // 2), 200) # Usar la clase Boss
                    self.visible_sprites.add(boss)
                    self.enemy_sprites.add(boss)

    def horizontal_movement_collision(self):
        player = self.player
        if not player.dashing:
            player.rect.x += player.direction.x * player.speed

        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0: 
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player
        player.apply_gravity()

        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0: 
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    def check_enemy_collisions(self):
        if self.player.attacking:
            for enemy in self.enemy_sprites:
                if enemy.status != 'die' and self.player.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage()

        hits = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
        valid_hits = [enemy for enemy in hits if enemy.status != 'die']
        
        if valid_hits:
            self.player.health -= 1
            if self.player.health <= 0:
                self.create_map(self.current_level_index) # Reiniciar mismo nivel

    def check_level_transition(self):
        # Si el jugador pasa el límite derecho del mapa
        if self.player.rect.right >= self.level_width - 50:
            self.current_level_index += 1
            self.create_map(self.current_level_index)

    def run(self):
        self.player.update()
        self.enemy_sprites.update(self.player)
        
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.check_enemy_collisions()
        self.check_level_transition() # Chequear si cambiamos de zona
        
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)