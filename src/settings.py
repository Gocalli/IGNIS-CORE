# Configuración del Juego
import pygame

# Pantalla
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "IGNIS CORE: La Última Llama"

# Colores (Estilo Dieselpunk / Alto Contraste)
# Fondo: Azul Noche / Oscuro
COLOR_BG = (10, 15, 25) 
# Elementos Interactivos: Óxido / Naranja
COLOR_PLAYER = (255, 100, 0)  
COLOR_PLATFORM = (100, 100, 110)
COLOR_TEXT = (200, 200, 200)
COLOR_HEAT_LOW = (255, 255, 0)
COLOR_HEAT_HIGH = (255, 50, 0)

# Físicas del Jugador
PLAYER_SPEED = 5
PLAYER_GRAVITY = 0.8
PLAYER_JUMP_FORCE = -16
PLAYER_FRICTION = -0.12  # Para la inercia

# Stats del Jugador
PLAYER_MAX_HEALTH = 100
PLAYER_MAX_HEAT = 100
HEAT_INCREASE_PER_HIT = 15
HEAT_COOLDOWN_RATE = 1     # Cuánto enfría pasivamente o al ventilar
HEAT_DAMAGE_RATE = 0.5     # Daño por sobrecalentamiento
ATTACK_COOLDOWN = 400      # ms

# Dash (Impulso)
PLAYER_DASH_SPEED = 15     # Velocidad durante el dash
PLAYER_DASH_DURATION = 200 # Cuánto dura el impulso (ms)
PLAYER_DASH_COOLDOWN = 1000 # Cuánto tarda en recargar (ms)

# Enemigos
ENEMY_SPEED = 3
ENEMY_DAMAGE = 20
ENEMY_ATTACK_DISTANCE = 150
ENEMY_ATTACK_COOLDOWN = 1000

# Tiles
TILE_SIZE = 16 # Mayor precisión (antes 32)
PLATFORM_TILE_WIDTH = 16
PLATFORM_TILE_HEIGHT = 16

# UI
UI_BAR_HEIGHT = 20
UI_HEALTH_BAR_WIDTH = 200
UI_HEAT_BAR_WIDTH = 200
UI_FONT_SIZE = 18
