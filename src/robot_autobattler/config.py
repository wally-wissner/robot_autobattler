import pathlib


_ROOT_DIRECTORY = pathlib.Path(__file__).parent


def absolute_path(path):
    path = path.lstrip("/")
    _absolute_path = pathlib.Path(_ROOT_DIRECTORY, path)
    return _absolute_path
