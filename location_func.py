from abc import abstractmethod, ABC
from typing import List
from path import Path


class LocationFunc(ABC):
    """
    Abstract base class for functionalities for locations where files can be stored
    """
    def __init__(self, base_path: str):
        self.base_path = base_path

    @abstractmethod
    def check_connection(self) -> bool:
        """
        This method checks the connection with the location.
        :return: true if location is accessible, false otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def is_dir(self, relative_path: str) -> bool:
        """
        This method checks if the path given is a directory
        :param relative_path: The relative path to the location
        :type relative_path: str
        :return: true if location is a directory, false otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def get_paths(self) -> List[Path]:
        """
        This method returns a list with all the paths that are in the location
        :return: a list with paths from location
        """
        raise NotImplementedError

    @abstractmethod
    def mkfile(self, relative_path: str, new_data: bytes) -> float:
        """
        This method is used to create a new file
        :param relative_path: the relative path to the file that is wanted to be created
        :type relative_path: str
        :param new_data: the data that is wanted to be inserted into the file
        :type new_data: bytes
        :return: mtime of the new file
        """
        raise NotImplementedError

    @abstractmethod
    def mkdir(self, relative_path: str) -> float:
        """
        This method is used to create a new directory
        :param relative_path: the relative path to the directory that is wanted to be created
        :type relative_path: str
        :return: mtime of the new file
        """
        raise NotImplementedError

    @abstractmethod
    def delete_dir(self, relative_path: str) -> bool:
        """
        This method is used to delete a directory
        :param relative_path: the relative path to the directory that is wanted to be deleted
        :type relative_path: str
        :return: true if the directory was deleted successfully, false otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, relative_path: str) -> bool:
        """
        This method is used to delete a file
        :param relative_path: the relative path to the file that is wanted to be deleted
        :type relative_path: str
        :return: true if the file was deleted successfully, false otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def replace(self, relative_path: str, new_data: bytes) -> float:
        """
        This method is used to replace data from a file that is located to relative_path
        :param relative_path: the relative path to the file which data is wanted to be replaced
        :type relative_path: str
        :param new_data: data to be inserted into the file instead of the old data
        :type new_data: bytes
        :return: mtime of the modified file
        """
        raise NotImplementedError

    @abstractmethod
    def get_data(self, relative_path: str) -> None | bytes:
        """
        This method extracts data from a file
        :param relative_path: the relative path to the file which data is wanted to be extracted
        :type relative_path: str
        :return: data extracted from the file
        """
        raise NotImplementedError
