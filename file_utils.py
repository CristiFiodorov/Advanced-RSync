import os
import time
import stat


def wait_file(file_path: str) -> bool:
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
