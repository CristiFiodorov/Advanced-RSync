class Path:
    def __init__(self, name, mtime, is_dir):
        self.name = name
        self.mtime = mtime
        self.is_dir = is_dir

    def __str__(self):
        return f"(name: {self.name}; mtime: {self.mtime}; is_dir: {self.is_dir})"

    def __repr__(self):
        return f"(name: {self.name}; mtime: {self.mtime}; is_dir: {self.is_dir})"
