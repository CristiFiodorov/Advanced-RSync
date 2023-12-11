import time
from find_changes import *


class SyncManager:
    def __init__(self, location_func1, location_func2):
        self.location_func = [location_func1, location_func2]
        self.files_map = dict()

    def init_sync(self):
        self.files_map = dict()
        paths1 = self.location_func[0].get_paths()
        paths2 = self.location_func[1].get_paths()

        for path1 in paths1:
            for path2 in paths2:
                if path1.name == path2.name:
                    # exists in both locations
                    if path1.is_dir:
                        self.files_map[path1.name] = [path1.mtime, path2.mtime, path1.is_dir]
                        break
                    if path1.mtime > path2.mtime:
                        self.files_map[path1.name] = [path1.mtime, 0, path1.is_dir]
                        data = self.location_func[0].get_data(path1.name)
                        if data:
                            self.files_map[path1.name][1] = self.location_func[1].replace(path1.name, data)
                    else:
                        self.files_map[path2.name] = [0, path2.mtime, path2.is_dir]
                        data = self.location_func[1].get_data(path2.name)
                        if data:
                            self.files_map[path2.name][0] = self.location_func[0].replace(path2.name, data)
                    # we found it and can break (also to not execute else)
                    break
            else:
                # file/folder exists only in path1 not in path2
                self.files_map[path1.name] = [path1.mtime, 0, path1.is_dir]
                if path1.is_dir:
                    self.files_map[path1.name][1] = self.location_func[1].mkdir(path1.name)
                else:
                    data = self.location_func[0].get_data(path1.name)
                    self.files_map[path1.name][1] = self.location_func[1].mkfile(path1.name, data)

        path1_names = [path.name for path in paths1]
        for path2 in paths2:
            if path2.name not in path1_names:
                # file/folder exists only in path2 not in path1
                self.files_map[path2.name] = [0, path2.mtime, path2.is_dir]
                if path2.is_dir:
                    self.files_map[path2.name][0] = self.location_func[0].mkdir(path2.name)
                else:
                    data = self.location_func[1].get_data(path2.name)
                    self.files_map[path2.name][0] = self.location_func[0].mkfile(path2.name, data)

    def sync_location(self, number):
        other_number = 1 if number == 0 else 0

        changes = find_changes(self.location_func[number], self.files_map, number)

        print(number, changes)

        for file_name, mtime, mod, is_dir in changes:
            if mod == ModificationType.MOD:
                self.files_map[file_name][number] = mtime
                if is_dir:
                    continue
                data = self.location_func[number].get_data(file_name)
                if data:
                    self.files_map[file_name][other_number] = self.location_func[other_number].replace(file_name, data)
            if mod == ModificationType.DEL:
                self.files_map.pop(file_name, None)
                if is_dir:
                    self.location_func[other_number].delete_dir(file_name)
                else:
                    self.location_func[other_number].delete_file(file_name)
            if mod == ModificationType.MK:
                self.files_map[file_name] = [0, 0, is_dir]
                self.files_map[file_name][number] = mtime
                if is_dir:
                    self.files_map[file_name][other_number] = self.location_func[other_number].mkdir(file_name)
                else:
                    data = self.location_func[number].get_data(file_name)
                    if data:
                        self.files_map[file_name][other_number] = self.location_func[other_number].mkfile(file_name, data)

    def sync(self):
        self.init_sync()

        while True:
            try:
                time.sleep(5)
                self.sync_location(0)
                self.sync_location(1)
            except KeyboardInterrupt as e:
                print("Exit")
                return
