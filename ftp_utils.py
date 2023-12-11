import time


def is_entry_directory(ftp, path):
    is_dir = False
    curr_path = ftp.pwd()
    try:
        ftp.cwd(path)
        is_dir = True
    except Exception as e:
        pass

    ftp.cwd(curr_path)
    return is_dir


def get_unix_timestamp(timestamp):
    year = int(timestamp[0:4])
    month = int(timestamp[4:6])
    day = int(timestamp[6:8])
    hour = int(timestamp[8:10])
    minute = int(timestamp[10:12])
    second = int(timestamp[12:14])

    unix_timestamp = int(time.mktime((year, month, day, hour, minute, second, 0, 0, -1)))

    return unix_timestamp


def recursive_ftp_delete(ftp, directory):
    ftp.cwd(directory)
    files = ftp.nlst()

    for file in files:
        if is_entry_directory(ftp, file):
            recursive_ftp_delete(ftp, file)
        else:
            ftp.delete(file)

    ftp.cwd("..")
    ftp.rmd(directory)