
def init_sync(location_func1, location_func2):
    paths1 = location_func1.get_paths()
    paths2 = location_func2.get_paths()

    path1_names = [path.name for path in paths1]
    path2_names = [path.name for path in paths2]

    for path1 in paths1:
        if path1.name not in path2_names:
            if path1.is_dir:
                location_func2.mkdir(path1.name)
            else:
                data = location_func1.get_data(path1.name)
                location_func2.mkfile(path1.name, data)

    for path2 in paths2:
        if path2.name not in path1_names:
            if path2.is_dir:
                location_func1.mkdir(path2.name)
            else:
                data = location_func2.get_data(path2.name)
                location_func1.mkfile(path2.name, data)
