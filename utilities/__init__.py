import os

def remove_path_prefix(path):
    """
    Remove '\\cn-sha-argo\' or '\\us-aus-argo\'
    from path
    """
    return path[14:]

def add_path_prefix(path, prefix):
    """
    Add '\\cn-sha-argo' or '\\us-aus-argo'
    to the begin of the path
    """
    return os.path.join(prefix, path)


