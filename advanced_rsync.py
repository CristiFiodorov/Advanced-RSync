from folder_func import *


def main():
    folder_f = FolderFunc('D:/Test')

    folder_f.mkdir('ceva')
    folder_f.mkfile('ceva/newgit_file.txt', b'Hello, World!')

    print(folder_f.get_paths())


if __name__ == '__main__':
    main()
