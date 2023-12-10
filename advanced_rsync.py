from folder_func import *
from ftp_func import *
from zip_func import *
from init_sync import init_sync
from find_changes import find_changes
import time


def main():
    zip_f = ZipFunc(r'D:\Test.zip')
    folder_f = FolderFunc(r'D:\Test')
    ftp_f = FtpFunc('/', '127.0.0.1', 'rsync-user', '123123')

    files_map = init_sync(zip_f, ftp_f)
    print(files_map)
    time.sleep(20)
    print(find_changes(ftp_f, files_map, 2))


if __name__ == '__main__':
    main()
