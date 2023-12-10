from folder_func import *
from ftp_func import *
from zip_func import *


def main():
    zip_f = ZipFunc(r'D:\Test.zip')

    zip_f.mkdir('pop')

    print(zip_f.get_paths())

    data = zip_f.get_data('Test/LOL.txt')

    zip_f.mkfile('pop/ceva.txt', data)

    zip_f.delete_dir('pop')

    zip_f.mkdir('pop2')

    zip_f.move_file('Test/LOL.txt', 'LOL.txt')

    zip_f.make('Test/LOL.txt', data)


if __name__ == '__main__':
    main()
