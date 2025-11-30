import pygame
from os import walk

def import_folder(path):
    surface_list = []
    
    for _, __, img_files in walk(path):
        # Ordenar para asegurar que los frames se carguen en orden correcto (ej. idle_0.png, idle_1.png)
        img_files.sort() 
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
            
    return surface_list

def import_spritesheet_row(path, frame_width, frame_height, num_frames):
    """
    Carga un sprite sheet de una sola fila y lo recorta en frames individuales.
    path: Ruta al archivo del sprite sheet.
    frame_width: Ancho de un frame individual.
    frame_height: Alto de un frame individual.
    num_frames: Número total de frames en el sprite sheet.
    """
    try:
        sheet = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f"Error al cargar el sprite sheet '{path}': {e}")
        return []

    frames = []
    for i in range(num_frames):
        x = i * frame_width
        y = 0 # Asumiendo una sola fila
        
        # Verificar que el recorte no se salga de los límites de la imagen
        if x + frame_width > sheet.get_width() or y + frame_height > sheet.get_height():
            print(f"Advertencia: Frame {i} se sale de los límites del sprite sheet en {path}. Recorte incompleto.")
            break # Detener si un frame se sale
            
        frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), pygame.Rect(x, y, frame_width, frame_height))
        frames.append(frame)
    return frames