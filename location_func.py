
class LocationFunc:
    def __init__(self, base_path):
        self.base_path = base_path

    def check_connection(self):
        raise NotImplementedError

    def is_dir(self, relative_path):
        raise NotImplementedError

    def get_paths(self):
        raise NotImplementedError

    def mkfile(self, relative_path, new_data):
        raise NotImplementedError

    def mkdir(self, relative_path):
        raise NotImplementedError

    def delete_dir(self, relative_path):
        raise NotImplementedError

    def delete_file(self, relative_path):
        raise NotImplementedError

    def replace(self, relative_path, new_data):
        raise NotImplementedError

    def get_data(self, relative_path):
        raise NotImplementedError
