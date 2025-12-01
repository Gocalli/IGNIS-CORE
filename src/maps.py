# Diseños de Nivel
# Ajustado para main_map.png con ALTA PRECISIÓN (32px grid)
# Altura 720px / 32px = ~22.5 filas -> Usaremos 23 filas
# Ancho ~5248px / 32px = ~164 columnas

# P = Player
# E = Enemy
# X = Pared/Plataforma

# Generamos un mapa base largo
row_empty = " " * 164
row_floor = "X" * 164

level_0 = [
    row_empty, # 0
    "XXX                                   XXXXXX", # 1
    "XXX                                   XXXXXX", # 2
    "XXX                                   XXXXXX", # 3
    "XXX                                   XXXXXX", # 4
    "XXX                                   XXXXXX", # 5
    "XXX                                   XXXXXX ", # 6
    "X             XXXXXXXXXXXXX           XXXXX     ", # 7
    "X                                      XXX", # 8
    "X", # 9
    "X       XXX", # 10
    "X", # 11
    "X      ", # 12
    "X                                      XXX                                      XXX                     ", # 13
    "XXXXXX                             XXXXX XXXXXX           XXXXX          XXXXXXXX XXX                    ", # 14
    "   X                                                                  XXX                             P   ", # 15
    "   X    XXXXXX                                 XXXXXXXX          XXXXX               XXXXXXXXXXXXXXXXXXX", # 16
    "   X              XXXXXX", # 17
    "   X", # 18
    "   X                        XXXXX", # 19
    "   X", # 20
    "   X                                                                                                                               ", # 21 (Entidades)
    row_floor, # 22 (Suelo)
]

levels = [level_0]