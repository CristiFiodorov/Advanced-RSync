import ftplib
from ftplib import FTP
from ftp_utils import *
from path import Path
from io import BytesIO


class FtpFunc:
    def __init__(self, base_path, host, username, password):
        self.base_path = base_path
        self.host = host
        self.username = username
        self.password = password

    def check_connection(self):
        try:
            with ftplib.FTP(self.host, self.username, self.password, timeout=10):
                return True
        except ftplib.all_errors as e:
            print(e)
            return False

    def is_dir(self, relative_path):
        if not self.check_connection():
            return False

        try:
            with FTP(self.host) as ftp:
                ftp.login(self.username, self.password)

                is_dir = is_entry_directory(ftp, relative_path)

                return is_dir
        except Exception as e:
            print(e)
            return False

    def get_paths(self):
        if not self.check_connection():
            return []

        try:
            with FTP(self.host) as ftp:
                ftp.login(self.username, self.password)
                ftp.cwd(self.base_path)

                paths = []

                def traverse_ftp_directory(directory):
                    ftp.cwd(directory)
                    files = ftp.nlst()

                    for file in files:
                        abs_path = directory + "/" + file
                        if directory == "/":
                            abs_path = abs_path[1:]

                        timestamp = ftp.sendcmd(f"MDTM {abs_path}")[4:]
                        mtime = get_unix_timestamp(timestamp)

                        path = Path(abs_path.replace("/", "\\")[1:], mtime, False)

                        if is_entry_directory(ftp, file):
                            path.is_dir = True
                            traverse_ftp_directory(abs_path)

                        paths.append(path)

                    ftp.cwd("..")

                traverse_ftp_directory(self.base_path)

                paths.reverse()
                return paths

        except Exception as e:
            print(e)
            return []

    def mkfile(self, relative_path, new_data):
        if not self.check_connection():
            return 0

        relative_path = relative_path.replace("\\", "/")
        try:
            with FTP(self.host) as ftp:
                ftp.login(self.username, self.password)
                abs_path = self.base_path + "/" + relative_path

                with BytesIO(new_data) as binary_data:
                    ftp.storbinary(f'STOR {abs_path}', binary_data)

                timestamp = ftp.sendcmd(f"MDTM {abs_path}")[4:]
                mtime = get_unix_timestamp(timestamp)

                print(f"File '{abs_path}'was created on the FTP server.")

                return mtime

        except Exception as e:
            print(e)
            return 0

    def mkdir(self, relative_path):
        if not self.check_connection():
            return 0

        relative_path = relative_path.replace("\\", "/")
        try:
            with FTP(self.host) as ftp:
                ftp.login(self.username, self.password)
                abs_path = self.base_path + "/" + relative_path

                ftp.mkd(abs_path)

                timestamp = ftp.sendcmd(f"MDTM {abs_path}")[4:]
                mtime = get_unix_timestamp(timestamp)

                print(f"Folder '{abs_path}' created on the FTP server.")

                return mtime

        except Exception as e:
            print(e)
            return 0

    def delete_dir(self, relative_path):
        if not self.check_connection():
            return False

        relative_path = relative_path.replace("\\", "/")
        try:
            with FTP(self.host) as ftp:
                ftp.login(self.username, self.password)

                recursive_ftp_delete(ftp, self.base_path + "/" + relative_path)

                print(f"Folder '{relative_path}' deleted from the FTP server.")

        except Exception as e:
            print(e)
            return False

        return True

    def delete_file(self, relative_path):
        if not self.check_connection():
            return False

        relative_path = relative_path.replace("\\", "/")
        try:
            with FTP(self.host) as ftp:
                ftp.login(self.username, self.password)
                abs_path = self.base_path + "/" + relative_path

                ftp.delete(abs_path)

                print(f"File '{abs_path}' deleted from the FTP server.")

        except Exception as e:
            print(e)
            return False

        return True

    def replace(self, relative_path, new_data):
        if not self.check_connection():
            return 0

        relative_path = relative_path.replace("\\", "/")
        try:
            with FTP(self.host) as ftp:
                ftp.login(self.username, self.password)
                if is_entry_directory(ftp, relative_path):
                    return 0

                abs_path = self.base_path + "/" + relative_path

                with BytesIO(new_data) as binary_data:
                    ftp.storbinary(f'STOR {abs_path}', binary_data)

                timestamp = ftp.sendcmd(f"MDTM {abs_path}")[4:]
                mtime = get_unix_timestamp(timestamp)

                print(f"File '{abs_path}' was modified on the FTP server.")

                return mtime

        except Exception as e:
            print(e)
            return 0

    def get_data(self, relative_path):
        if not self.check_connection():
            return None

        relative_path = relative_path.replace("\\", "/")
        try:
            with FTP(self.host) as ftp:
                ftp.login(self.username, self.password)
                abs_path = self.base_path + "/" + relative_path

                r = BytesIO()
                ftp.retrbinary(f'RETR {abs_path}', r.write)

                return r.getvalue()

        except Exception as e:
            print(e)
            return None

    def move(self, relative_path, relative_dest_path):
        if not self.check_connection():
            return 0

        try:
            with FTP(self.host) as ftp:
                ftp.login(self.username, self.password)
                abs_path = self.base_path + "/" + relative_path
                abs_dest_path = self.base_path + "/" + relative_dest_path

                ftp.rename(abs_path, abs_dest_path)

                timestamp = ftp.sendcmd(f"MDTM {abs_dest_path}")[4:]
                mtime = get_unix_timestamp(timestamp)

                print(f"File '{abs_path}' was moved to {abs_dest_path} on the FTP server.")

                return mtime

        except Exception as e:
            print(e)
            return 0

    def move_dir(self, relative_path, relative_dest_path):
        return self.move(relative_path.replace("\\", "/"), relative_dest_path.replace("\\", "/"))

    def move_file(self, relative_path, relative_dest_path):
        return self.move(relative_path.replace("\\", "/"), relative_dest_path.replace("\\", "/"))