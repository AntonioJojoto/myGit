import os

def repo_path(repo, *path):
    """Compute path under repo's gitdir."""
    return os.path.join(repo.gitdir, *path)

def repo_dir(repo, *path, mkdir=False):
    """Same as repo_path, but mkdir *path if absent if mkdir."""
    path_full = repo_path(repo, *path)

    if os.path.exists(path_full):
        if os.path.isdir(path_full):
            return path_full
        else:
            raise Exception(f"Not a directory {path_full}")

    if mkdir:
        print(f"Creating directory: {path_full}")
        print("Full path is ",path_full)
        os.makedirs(path_full)
        return path_full
    else:
        return None

def repo_file(repo, *path, mkdir=False):
    """Compute path under repo's gitdir, create dirname(*path) if absent."""
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)
    return None

