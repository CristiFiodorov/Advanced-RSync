import logging
import zipfile
import os
from datetime import datetime
from typing import List
from location_func import LocationFunc
from path import Path
import time


logger = logging.getLogger(__name__)


class ZipFunc(LocationFunc):
    def __init__(self, base_path: str):
        super().__init__(base_path)

    def check_connection(self) -> bool:
        try:
            with zipfile.ZipFile(self.base_path, 'r'):
                return True
        except Exception as e:
            logger.error(e)
            return False

    def is_dir(self, relative_path: str) -> bool:
        if not self.check_connection():
            return False
        try:
            with zipfile.ZipFile(self.base_path, 'r') as zip_file:
                return zip_file.getinfo(relative_path).is_dir()
        except Exception as e:
            logger.error(e)
            return False

    def get_paths(self) -> List[Path]:
        try:
            paths = []
            with zipfile.ZipFile(self.base_path, 'r') as zip_file:
                for item in zip_file.infolist():
                    name = item.filename
                    mtime = datetime(*item.date_time).timestamp()
                    is_dir = self.is_dir(name)
                    if is_dir:
                        name = name[:-1]
                    paths.append(Path(name.replace("/", "\\"), mtime, is_dir))
            return paths
        except Exception as e:
            logger.error(e)
            return []

    def _make(self, relative_path: str, new_data: bytes) -> float:
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
        except Exception as e:
            logger.error(e)
            return 0

    def mkfile(self, relative_path: str, new_data: bytes) -> float:
        return self._make(relative_path.replace("\\", "/"), new_data)

    def mkdir(self, relative_path: str) -> float:
        if not relative_path.endswith("/"):
            relative_path += "/"
        return self._make(relative_path.replace("\\", "/"), b"")

    def _delete(self, relative_path: str) -> bool:
        if not self.check_connection():
            return False
        try:
            temp_zip_file_path = os.path.expanduser(f"{self.base_path}temp")
            with zipfile.ZipFile(self.base_path, 'r') as zip_file:
                with zipfile.ZipFile(temp_zip_file_path, 'w') as temp_zip_file:
                    for item in zip_file.infolist():
                        if (not self.is_dir(relative_path) and item.filename != relative_path) or \
                                (self.is_dir(relative_path) and not item.filename.startswith(relative_path)):
                            data = zip_file.read(item.filename)
                            temp_zip_file.writestr(item, data)
        except Exception as e:
            logger.error(e)
            return False

        while True:
            try:
                # fails to replace if the zip is opened !!!!!!
                os.replace(temp_zip_file_path, self.base_path)
            except PermissionError:
                continue
            return True

    def delete_dir(self, relative_path: str) -> bool:
        if not relative_path.endswith("/"):
            relative_path += "/"
        return self._delete(relative_path.replace("\\", "/"))

    def delete_file(self, relative_path: str) -> bool:
        return self._delete(relative_path.replace("\\", "/"))

    def replace(self, relative_path: str, new_data: bytes) -> float:
        self.delete_file(relative_path)
        return self.mkfile(relative_path, new_data)

    def get_data(self, relative_path: str) -> None | bytes:
        if not self.check_connection():
            return None
        try:
            with zipfile.ZipFile(self.base_path, 'r') as zip_file:
                data = zip_file.read(relative_path.replace("\\", "/"))

            return data
        except Exception as e:
            logger.error(e)
            return None
