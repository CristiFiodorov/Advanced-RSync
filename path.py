class Path:
    """
    This class represent a location on a file system
    """
    def __init__(self, name: str, mtime: float, is_dir: bool):
        """
        Initialize a new Path instance
        :param name: the path to file/folder in the file system
        :type name: str
        :param mtime: modification time of file/folder
        :type mtime: float
        :param is_dir: a boolean that represent if the path is a file or folder
        :type is_dir: bool
        """
        self.name = name
        self.mtime = mtime
        self.is_dir = is_dir

    def __str__(self) -> str:
        return f"(name: {self.name}; mtime: {self.mtime}; is_dir: {self.is_dir})"

    def __repr__(self) -> str:
        return f"(name: {self.name}; mtime: {self.mtime}; is_dir: {self.is_dir})"
