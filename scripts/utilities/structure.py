from os.path import join

from config import ROOT_DIRECTORY


def absolute_path(path):
    return join(ROOT_DIRECTORY, path)
