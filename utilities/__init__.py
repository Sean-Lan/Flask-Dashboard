import os
import re

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


def get_date(folder_name):
    date_pattern = re.compile(r'\d{4}_?\d{2}_?\d{2}_\d{4}')
    match = date_pattern.search(folder_name)
    return match.group()

def get_stack_date(stack_name):
    date_pattern = re.compile(r'\d{8}_\d+[dabf]\d+')
    match = date_pattern.search(stack_name)
    return match.group()
