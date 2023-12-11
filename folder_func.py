import os
from typing import List
from file_utils import wait_file
import time
from location_func import LocationFunc
from path import Path
import shutil


class FolderFunc(LocationFunc):
    def __init__(self, base_path):
        super().__init__(base_path)

    def check_connection(self) -> bool:
        return os.path.isdir(self.base_path)

    def is_dir(self, relative_path: str) -> bool:
        abs_path = os.path.join(self.base_path, relative_path)
        return os.path.isdir(abs_path)

    def get_paths(self) -> List[Path]:
        if not self.check_connection():
            return []

        paths_name = []
        for root, directories, files in os.walk(self.base_path):
            paths_name.extend([os.path.join(root, directory) for directory in directories])
            paths_name.extend([os.path.join(root, file) for file in files])

        paths = []
        for path_name in paths_name:
            name = os.path.relpath(path_name, self.base_path)
            mtime = os.path.getmtime(path_name)
            is_dir = os.path.isdir(path_name)
            path = Path(name, mtime, is_dir)
            paths.append(path)

        return paths

    def mkfile(self, relative_path: str, new_data: bytes) -> float:
        if not self.check_connection():
            return 0

        abs_path = os.path.join(self.base_path, relative_path)

        if os.path.exists(abs_path):
            return 0

        with open(abs_path, "wb") as file:
            file.write(new_data)

        mtime = 0
        if wait_file(abs_path):
            mtime = os.path.getmtime(abs_path)

        return mtime

    def mkdir(self, relative_path: str) -> float:
        if not self.check_connection():
            return 0

        abs_path = os.path.join(self.base_path, relative_path)

        if os.path.exists(abs_path):
            return 0

        try:
            os.mkdir(abs_path)
            time.sleep(1)

            return os.path.getmtime(abs_path)
        except FileNotFoundError as e:
            print(e)
            return 0

    def _delete(self, relative_path: str) -> bool:
        if not self.check_connection():
            return False

        abs_path = os.path.join(self.base_path, relative_path)

        if not os.path.exists(abs_path):
            return False

        if os.path.isdir(abs_path):
            shutil.rmtree(abs_path)
        else:
            os.remove(abs_path)

        return True

    def delete_dir(self, relative_path: str) -> bool:
        return self._delete(relative_path)

    def delete_file(self, relative_path: str) -> bool:
        return self._delete(relative_path)

    def replace(self, relative_path: str, new_data: bytes) -> float:
        if not self.check_connection():
            return 0

        abs_path = os.path.join(self.base_path, relative_path)

        if not os.path.exists(abs_path):
            return 0

        with open(abs_path, "wb") as file:
            file.write(new_data)
        time.sleep(1)

        return os.path.getmtime(abs_path)

    def get_data(self, relative_path: str) -> None | bytes:
        if not self.check_connection():
            return None

        abs_path = os.path.join(self.base_path, relative_path)

        if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
            return None

        with open(abs_path, "rb") as file:
            data = file.read()

        return data
