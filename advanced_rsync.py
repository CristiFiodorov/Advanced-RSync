import logging
from folder_func import *
from ftp_func import *
from zip_func import *
from sync_manager import *
import sys


logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='advanced_rsync.log',
        filemode='w'
    )


def get_location_func(location: str) -> LocationFunc | None:
    """
    This function receives a string representing the location that will be monitored.
    The following formats are accepted:
        - ftp:user:password@URL/base_path
        - zip:base_path
        - folder:base_path
    :param location: string representation of the location
    :type location: str
    :return: A class with all the functionality for the location
    """
    parts = location.split(":", 1)
    if len(parts) < 2:
        return None
    location_type = parts[0]

    if location_type == "folder":
        folder_func = FolderFunc(parts[1])
        return folder_func if folder_func.check_connection() else None
    if location_type == "zip":
        zip_func = ZipFunc(parts[1])
        return zip_func if zip_func.check_connection() else None
    if location_type == "ftp":
        path_parts = parts[1].split("@", 1)
        if len(path_parts) < 2:
            return None
        credentials = path_parts[0].split(":", 1)
        if len(credentials) < 2:
            return None
        user = credentials[0]
        password = credentials[1]
        path = path_parts[1].split("/", 1)
        host = path[0]
        base_path = "/"
        if len(path) > 1:
            base_path += path[1]

        ftp_func = FtpFunc(base_path, host, user, password)
        return ftp_func if ftp_func.check_connection() else None


def main():
    if len(sys.argv) != 3:
        logging.error("The system accepts only two arguments!")
        return -1

    location_func1 = get_location_func(sys.argv[1])
    if location_func1 is None:
        logging.error("First location provided cannot be accessed")
        return -1

    location_func2 = get_location_func(sys.argv[2])
    if location_func1 is None:
        logging.error("Second location provided cannot be accessed")
        return -1

    sync_manager = SyncManager(location_func1, location_func2)
    sync_manager.sync()


if __name__ == '__main__':
    main()
