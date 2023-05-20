from csv import reader
from pathlib import Path

def import_csv_layout(path: Path):
    terrain_map = []
    with open(path, 'r') as level_map: 
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(row)
        return terrain_map