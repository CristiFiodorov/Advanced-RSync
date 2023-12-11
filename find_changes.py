from enum import Enum, auto
from location_func import *
from typing import List, Tuple


class ModificationType(Enum):
    MOD = auto()
    DEL = auto()
    MK = auto()


def find_changes(location_func: LocationFunc, files_map: dict, number: int) -> List[Tuple]:
    result = []
    items1 = [*files_map.items()]
    items2 = location_func.get_paths()

    for file_path, data in items1:
        for item in items2:
            if item.name == file_path:
                if item.mtime != data[number] and data[number] > 0:
                    result.append((file_path, item.mtime, ModificationType.MOD, item.is_dir))
                break
        else:
            # are in files_map but already does not exist in file location
            result.append((file_path, data[number], ModificationType.DEL, data[2]))

    diff = set(item2 for item2 in items2 if item2.name not in [item1[0] for item1 in items1])
    for item in diff:
        # are in file location but not in file_map
        result.append((item.name, item.mtime, ModificationType.MK, item.is_dir))

    return result
