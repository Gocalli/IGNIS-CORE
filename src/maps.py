# Diseños de Nivel
# Ajustado para main_map.png escalado (aprox 5220x720)
# Tile size 64px -> ~82 columnas x 11 filas

# P = Player
# E = Enemy
# X = Pared/Plataforma

level_0 = [
    "X" + " " * 80 + "X", # 0
    "X" + " " * 80 + "X", # 1
    "X" + " " * 80 + "X", # 2
    "X" + " " * 80 + "X", # 3
    "X" + " " * 80 + "X", # 4
    "X" + " " * 80 + "X", # 5
    "X" + " " * 80 + "X", # 6
    "X" + " " * 80 + "X", # 7
    "X        E         E         E         E         E         E         E        X", # 8
    "X P                                                                           X", # 9
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", # 10 (Suelo)
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", # 11
]

levels = [level_0]