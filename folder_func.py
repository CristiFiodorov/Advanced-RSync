import os
from file_utils import wait_file
import time
from path import Path
import shutil


class FolderFunc:
    def __init__(self, base_path):
        self.base_path = base_path

    def is_entry_directory(self, relative_path):
        abs_path = os.path.join(self.base_path, relative_path)
        return os.path.isdir(abs_path)

    def get_paths(self):
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

    def mkfile(self, relative_path, new_data):
        abs_path = os.path.join(self.base_path, relative_path)

        if os.path.exists(abs_path):
            return 0

        with open(abs_path, "wb") as file:
            file.write(new_data)

        mtime = 0
        if wait_file(abs_path):
            mtime = os.path.getmtime(abs_path)

        return mtime

    def mkdir(self, relative_path):
        abs_path = os.path.join(self.base_path, relative_path)

        if os.path.exists(abs_path):
            return 0

        os.mkdir(abs_path)
        time.sleep(1)

        return os.path.getmtime(abs_path)

    def delete(self, relative_path):
        abs_path = os.path.join(self.base_path, relative_path)

        if not os.path.exists(abs_path):
            return

        if os.path.isdir(abs_path):
            shutil.rmtree(abs_path)
        else:
            os.remove(abs_path)

    def delete_dir(self, relative_path):
        self.delete(relative_path)

    def delete_file(self, relative_path):
        self.delete(relative_path)

    def replace(self, relative_path, new_data):
        abs_path = os.path.join(self.base_path, relative_path)

        if not os.path.exists(abs_path):
            return 0

        with open(abs_path, "wb") as file:
            file.write(new_data)
        time.sleep(1)

        return os.path.getmtime(abs_path)

    def get_data(self, relative_path):
        abs_path = os.path.join(self.base_path, relative_path)

        if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
            return None

        with open(abs_path, "rb") as file:
            data = file.read()

        return data

    def move(self, relative_path, relative_dest_path):
        abs_path = os.path.join(self.base_path, relative_path)
        abs_dest_path = os.path.join(self.base_path, relative_dest_path)

        if not os.path.exists(abs_path) and os.path.exists(abs_dest_path):
            return 0

        os.rename(abs_path, abs_dest_path)
        time.sleep(1)

        return os.path.getmtime(abs_dest_path)

    def move_dir(self, relative_path, relative_dest_path):
        return self.move(relative_path, relative_dest_path)

    def move_file(self, relative_path, relative_dest_path):
        return self.move(relative_path, relative_dest_path)
