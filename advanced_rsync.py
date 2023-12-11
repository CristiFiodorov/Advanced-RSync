from folder_func import *
from ftp_func import *
from zip_func import *
from sync_manager import *


def main():
    zip_f = ZipFunc(r'D:\Test.zip')
    folder_f = FolderFunc(r'D:\Test')
    ftp_f = FtpFunc('/', '127.0.0.1', 'rsync-user', '123123')

    sync_manager = SyncManager(zip_f, ftp_f)

    sync_manager.sync()


if __name__ == '__main__':
    main()
