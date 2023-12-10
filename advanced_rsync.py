from folder_func import *
from ftp_func import *
from zip_func import *
from init_sync import init_sync


def main():
    zip_f = ZipFunc(r'D:\Test.zip')
    folder_f = FolderFunc(r'D:\Test')
    ftp_f = FtpFunc('/', '127.0.0.1', 'rsync-user', '123123')

    files_map = init_sync(zip_f, ftp_f)
    print(files_map)


if __name__ == '__main__':
    main()
