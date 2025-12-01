# Diseños de Nivel
# Ajustado para pantalla 1280x720 (aprox 20x11 bloques de 64px)

# P = Player (Posición inicial)
# E = Enemy
# X = Pared/Plataforma (Invisible, colisión)

# Mapa ajustado visualmente a 'dash_map.jpg'
# La pantalla tiene 20 columnas de ancho (1280/64) y ~11 filas de alto (720/64)

level_0 = [
    "X                  X", # 0 (Techo/Aire)
    "X                  X", # 1
    "X                  X", # 2
    "X        XXXX      X", # 3 (Plataforma central superior - Motor)
    "X                  X", # 4
    "X                  X", # 5
    "X                  X", # 6
    "XXX       XXXX     X", # 7 (Plataformas laterales flotantes)
    "X   XXX            X", # 8
    "X P                X", # 9 (Jugador cerca del suelo)
    "XXXXXXXXXXXXXXXXXXXX", # 10 (Suelo principal)
    "XXXXXXXXXXXXXXXXXXXX", # 11 (Margen inferior)
]

# Placeholder para nivel 2
level_1 = [
    "X                  X",
    "X                  X",
    "X                  X",
    "X        XX        X",
    "X       XXXX       X",
    "X      XX  XX      X",
    "X                  X",
    "X   E          E   X",
    "XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXX",
]

levels = [level_0, level_1]