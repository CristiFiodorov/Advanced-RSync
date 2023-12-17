import os
import time
import stat


def wait_file(file_path: str) -> bool:
    """
    This function gets a path to a file and waits file to be created or to be accessible
    :param file_path: path to a file
    :type file_path: str
    :return: A true if file could be accessed, false if otherwise
    """
    for i in range(0, 10):
        try:
            with open(file_path, "rb"):
                return True
        except FileNotFoundError:
            time.sleep(1)
            continue
        except PermissionError:
            os.chmod(file_path, stat.S_IREAD | stat.S_IWRITE)
            time.sleep(1)
            continue

    return False
