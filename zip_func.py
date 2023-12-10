import zipfile
import os
from datetime import datetime
from path import Path
import time


class ZipFunc:
    def __init__(self, base_path):
        self.base_path = base_path

    def check_connection(self):
        try:
            with zipfile.ZipFile(self.base_path, 'r'):
                return True
        except:
            return False

    def is_dir(self, relative_path):
        if not self.check_connection():
            return False
        try:
            with zipfile.ZipFile(self.base_path, 'r') as zip_file:
                return zip_file.getinfo(relative_path).is_dir()
        except:
            return False

    def get_paths(self):
        try:
            paths = []
            with zipfile.ZipFile(self.base_path, 'r') as zip_file:
                for item in zip_file.infolist():
                    print(item.filename)
                    name = item.filename
                    mtime = datetime(*item.date_time).timestamp()
                    is_dir = self.is_dir(name)
                    if is_dir:
                        name = name[:-1]
                    paths.append(Path(name.replace("/", "\\"), mtime, is_dir))

            return paths
        except:
            return []

    def make(self, relative_path, new_data):
        if not self.check_connection():
            return 0
        try:
            mtime = 0
            with zipfile.ZipFile(self.base_path, 'a') as zip_file:
                if relative_path.replace("\\", "/") not in zip_file.namelist():
                    zip_info = zipfile.ZipInfo(relative_path)
                    zip_file.writestr(zip_info, new_data)
                    zip_info.date_time = time.localtime(time.time())
                    mtime = time.mktime(zip_info.date_time)

            return mtime
        except:
            return 0

    def mkfile(self, relative_path, new_data):
        return self.make(relative_path.replace("\\", "/"), new_data)

    def mkdir(self, relative_path):
        if not relative_path.endswith("/"):
            relative_path += "/"
        return self.make(relative_path.replace("\\", "/"), "")

    def delete(self, relative_path):
        if not self.check_connection():
            return False
        try:
            temp_zip_file_path = os.path.expanduser(f"{self.base_path}temp")
            with zipfile.ZipFile(self.base_path, 'r') as zip_file:
                with zipfile.ZipFile(temp_zip_file_path, 'w') as temp_zip_file:
                    for item in zip_file.infolist():
                        print(item.filename)
                        if (not self.is_dir(relative_path) and item.filename != relative_path) or \
                                (self.is_dir(relative_path) and not item.filename.startswith(relative_path)):
                            data = zip_file.read(item.filename)
                            temp_zip_file.writestr(item, data)
        except Exception as e:
            print(e)
            return False

        while True:
            try:
                # fails to replace if the zip is opened !!!!!!
                os.replace(temp_zip_file_path, self.base_path)
            except PermissionError:
                continue
            return True

    def delete_dir(self, relative_path):
        if not relative_path.endswith("/"):
            relative_path += "/"
        return self.delete(relative_path.replace("\\", "/"))

    def delete_file(self, relative_path):
        return self.delete(relative_path.replace("\\", "/"))

    def replace(self, relative_path, new_data):
        self.delete_file(relative_path)
        return self.mkfile(relative_path, new_data)

    def get_data(self, relative_path):
        if not self.check_connection():
            return None
        try:
            with zipfile.ZipFile(self.base_path, 'r') as zip_file:
                data = zip_file.read(relative_path.replace("\\", "/"))

            return data
        except KeyError:
            return None

    def move(self, relative_path, relative_dest_path):
        if not self.check_connection():
            return 0
        mtime = 0
        try:
            with zipfile.ZipFile(self.base_path, 'a') as zip_file:
                data = zip_file.read(relative_path)
                zip_info = zipfile.ZipInfo(relative_dest_path)
                zip_file.writestr(zip_info, data)
                zip_info.date_time = time.localtime(time.time())
                mtime = time.mktime(zip_info.date_time)
        except Exception as e:
            print(e)

        self.delete(relative_path)
        return mtime

    def move_dir(self, relative_path, relative_dest_path):
        if not relative_path.endswith("/"):
            relative_path += "/"
        if not relative_dest_path.endswith("/"):
            relative_dest_path += "/"
        return self.move(relative_path.replace("\\", "/"), relative_dest_path.replace("\\", "/"))

    def move_file(self, relative_path, relative_dest_path):
        return self.move(relative_path.replace("\\", "/"), relative_dest_path.replace("\\", "/"))