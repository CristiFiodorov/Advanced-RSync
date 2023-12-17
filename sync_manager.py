import time
import logging
from find_changes import *
from location_func import *

_logger = logging.getLogger(__name__)


class SyncManager:
    """
    This class takes 2 LocationFunc and synchronize the location represented by them and keeps the sync.
    """
    def __init__(self, location_func1: LocationFunc, location_func2: LocationFunc):
        """
        Initialize a new SyncManager instance

        :param location_func1: functionality class for first location
        :type location_func1: LocationFunc
        :param location_func2: functionality class for second location
        :type location_func2: LocationFunc
        """
        self.location_func = [location_func1, location_func2]
        self.files_map = dict()

    def _init_sync(self):
        self.files_map = dict()
        paths1 = self.location_func[0].get_paths()
        paths2 = self.location_func[1].get_paths()

        for path1 in paths1:
            for path2 in paths2:
                if path1.name == path2.name:
                    # exists in both locations
                    if path1.is_dir:
                        _logger.info(f"Folder {path1.name} exists in both locations!")
                        self.files_map[path1.name] = [path1.mtime, path2.mtime, path1.is_dir]
                        break
                    if path1.mtime > path2.mtime:
                        _logger.info(f"File {path1.name} exists in both location, but {self.location_func[0].base_path}"
                                    f" has the newest version. {path1.name} will be copied to "
                                    f"{self.location_func[1].base_path}")
                        self.files_map[path1.name] = [path1.mtime, 0, path1.is_dir]
                        data = self.location_func[0].get_data(path1.name)
                        if data:
                            self.files_map[path1.name][1] = self.location_func[1].replace(path1.name, data)
                    else:
                        _logger.info(f"File {path1.name} exists in both location, but {self.location_func[1].base_path}"
                                    f" has the newest version. {path1.name} will be copied to "
                                    f"{self.location_func[0].base_path}")
                        self.files_map[path2.name] = [0, path2.mtime, path2.is_dir]
                        data = self.location_func[1].get_data(path2.name)
                        if data:
                            self.files_map[path2.name][0] = self.location_func[0].replace(path2.name, data)
                    # we found it and can break (also to not execute else)
                    break
            else:
                # file/folder exists only in path1 not in path2
                _logger.info(f"File/Folder {path1.name} exists only in {self.location_func[0].base_path}. "
                            f"{path1.name} will be copied to {self.location_func[1].base_path}")
                self.files_map[path1.name] = [path1.mtime, 0, path1.is_dir]
                if path1.is_dir:
                    self.files_map[path1.name][1] = self.location_func[1].mkdir(path1.name)
                else:
                    data = self.location_func[0].get_data(path1.name)
                    if data:
                        self.files_map[path1.name][1] = self.location_func[1].mkfile(path1.name, data)

        path1_names = [path.name for path in paths1]
        for path2 in paths2:
            if path2.name not in path1_names:
                # file/folder exists only in path2 not in path1
                _logger.info(f"File/Folder {path2.name} exists only in {self.location_func[1].base_path}. "
                            f"{path2.name} will be copied to {self.location_func[0].base_path}")
                self.files_map[path2.name] = [0, path2.mtime, path2.is_dir]
                if path2.is_dir:
                    self.files_map[path2.name][0] = self.location_func[0].mkdir(path2.name)
                else:
                    data = self.location_func[1].get_data(path2.name)
                    if data:
                        self.files_map[path2.name][0] = self.location_func[0].mkfile(path2.name, data)

    def _sync_location(self, number: int):
        other_number = 1 if number == 0 else 0

        changes = find_changes(self.location_func[number], self.files_map, number)
        if len(changes) == 0:
            return

        _logger.info(f"Location {self.location_func[number].base_path} has the following changes: {changes}")

        for file_name, mtime, mod, is_dir in changes:
            if mod == ModificationType.MOD:
                _logger.info(f"{file_name} has been modified in {self.location_func[number].base_path}. "
                            f"Changes has been copied to {self.location_func[other_number].base_path}")
                self.files_map[file_name][number] = mtime
                if is_dir:
                    continue
                data = self.location_func[number].get_data(file_name)
                if data:
                    self.files_map[file_name][other_number] = self.location_func[other_number].replace(file_name, data)
            if mod == ModificationType.DEL:
                _logger.info(f"{file_name} has been deleted in {self.location_func[number].base_path}. "
                            f"File/Folder is being deleted in {self.location_func[other_number].base_path}")
                self.files_map.pop(file_name, None)
                if is_dir:
                    self.location_func[other_number].delete_dir(file_name)
                else:
                    self.location_func[other_number].delete_file(file_name)
            if mod == ModificationType.MK:
                _logger.info(f"{file_name} has been created in {self.location_func[number].base_path}. "
                            f"File/Folder is being created in {self.location_func[other_number].base_path}")
                self.files_map[file_name] = [0, 0, is_dir]
                self.files_map[file_name][number] = mtime
                if is_dir:
                    self.files_map[file_name][other_number] = self.location_func[other_number].mkdir(file_name)
                else:
                    data = self.location_func[number].get_data(file_name)
                    if data:
                        self.files_map[file_name][other_number] = self.location_func[other_number].mkfile(file_name, data)

    def sync(self):
        """
        This method makes the initial synchronisation between the two location and keep them sync
        """
        self._init_sync()

        while True:
            try:
                time.sleep(5)
                self._sync_location(0)
                self._sync_location(1)
            except KeyboardInterrupt as e:
                print("Exit")
                break
