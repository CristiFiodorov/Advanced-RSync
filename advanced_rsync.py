from folder_func import *
from ftp_func import *


def main():
    ftp_f = FtpFunc('/', '127.0.0.1', 'rsync-user', '123123')

    print(ftp_f.check_connection())
    ftp_f.delete_dir('ceva')

    ftp_f.mkdir('ceva')

    ftp_f.mkdir('ceva/altceva')

    print(ftp_f.is_entry_directory('ceva'))

    ftp_f.mkfile('ceva/altceva/file.txt', b'Hello, aici')

    ftp_f.replace('ceva/altceva/file.txt', b'Hello, acolo')

    print(ftp_f.get_paths())

    ftp_f.move_file('ceva/altceva/file.txt', 'ceva/file2.txt')

    print(ftp_f.get_paths())

    print(ftp_f.get_data('ceva/file2.txt'))


if __name__ == '__main__':
    main()
