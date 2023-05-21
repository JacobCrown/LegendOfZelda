from csv import reader
from os import walk
from pathlib import Path

import pygame

import common.constants as c


def import_csv_layout(path: Path):
    terrain_map = []
    with open(path, 'r') as level_map: 
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(row)
        return terrain_map


def import_folder(path: Path):
    surface_list = []

    for _, __, img_filenames in walk(path):
        for img in img_filenames:
            full_path = path / img
            image_surf = pygame.image.load(full_path)
            surface_list.append(image_surf)
    
    return surface_list
            

import_folder(c.PROJECT_DIRPATH / 'graphics/Grass')