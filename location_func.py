from typing import List
from path import Path


class LocationFunc:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def check_connection(self) -> bool:
        raise NotImplementedError

    def is_dir(self, relative_path: str) -> bool:
        raise NotImplementedError

    def get_paths(self) -> List[Path]:
        raise NotImplementedError

    def mkfile(self, relative_path: str, new_data: bytes) -> float:
        raise NotImplementedError

    def mkdir(self, relative_path: str) -> float:
        raise NotImplementedError

    def delete_dir(self, relative_path: str) -> bool:
        raise NotImplementedError

    def delete_file(self, relative_path: str) -> bool:
        raise NotImplementedError

    def replace(self, relative_path: str, new_data: bytes) -> float:
        raise NotImplementedError

    def get_data(self, relative_path: str) -> None | bytes:
        raise NotImplementedError
