
def init_sync(location_func1, location_func2):
    files_map = dict()
    paths1 = location_func1.get_paths()
    paths2 = location_func2.get_paths()

    for path1 in paths1:
        for path2 in paths2:
            if path1.name == path2.name:
                # exists in both locations
                if path1.is_dir:
                    files_map[path1.name] = [path1.mtime, path2.mtime, path1.is_dir]
                    break
                if path1.mtime > path2.mtime:
                    files_map[path1.name] = [path1.mtime, 0, path1.is_dir]
                    data = location_func1.get_data(path1.name)
                    files_map[path1.name][1] = location_func2.replace(path1.name, data)
                else:
                    files_map[path2.name] = [0, path2.mtime, path2.is_dir]
                    data = location_func2.get_data(path2.name)
                    files_map[path2.name][0] = location_func1.replace(path2.name, data)
                # we found it and can break (also to not execute else)
                break
        else:
            # file/folder exists only in path1 not in path2
            files_map[path1.name] = [path1.mtime, 0, path1.is_dir]
            if path1.is_dir:
                files_map[path1.name][1] = location_func2.mkdir(path1.name)
            else:
                data = location_func1.get_data(path1.name)
                files_map[path1.name][1] = location_func2.mkfile(path1.name, data)

    path1_names = [path.name for path in paths1]
    for path2 in paths2:
        if path2.name not in path1_names:
            # file/folder exists only in path2 not in path1
            files_map[path2.name] = [0, path2.mtime, path2.is_dir]
            if path2.is_dir:
                files_map[path2.name][0] = location_func1.mkdir(path2.name)
            else:
                data = location_func2.get_data(path2.name)
                files_map[path2.name][0] = location_func1.mkfile(path2.name, data)

    return files_map