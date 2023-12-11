import time
from ftplib import FTP


def is_entry_directory(ftp: FTP, path: str) -> bool:
    """
    This function checks if the path is a directory in the given FTP
    :param ftp: instance of FTP from ftplib
    :type ftp: FTP
    :param path: the path is wanted to be checked
    :type path: str
    :return: true if location is a directory, false otherwise
    """
    is_dir = False
    curr_path = ftp.pwd()
    try:
        ftp.cwd(path)
        is_dir = True
    except Exception as e:
        pass

    ftp.cwd(curr_path)
    return is_dir


def get_unix_timestamp(timestamp: str) -> float:
    """
    This function converts from a string representation of a timestamp to unix timestamp
    :param timestamp: string representation of a timestamp
    :return: unix timestamp
    """
    year = int(timestamp[0:4])
    month = int(timestamp[4:6])
    day = int(timestamp[6:8])
    hour = int(timestamp[8:10])
    minute = int(timestamp[10:12])
    second = int(timestamp[12:14])

    unix_timestamp = time.mktime((year, month, day, hour, minute, second, 0, 0, -1))

    return unix_timestamp


def recursive_ftp_delete(ftp: FTP, directory: str):
    """
    This function deletes a directory recursively
    :param ftp: instance of FTP from ftplib
    :type ftp: FTP
    :param directory: path to the directory that is wanted to be deleted
    """
    ftp.cwd(directory)
    files = ftp.nlst()

    for file in files:
        if is_entry_directory(ftp, file):
            recursive_ftp_delete(ftp, file)
        else:
            ftp.delete(file)

    ftp.cwd("..")
    ftp.rmd(directory)
