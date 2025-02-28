import os
import configparser
from os.path import isdir

from repository.GitRepository import GitRepository
from utils.path import repo_file,repo_dir

def repo_create(path):
    """ 
    Create a new repository at path.

    Parameters:
    path: Work directory in which the repo will be created

    Returns:
    GitRepository object of the created repo
    """

    repo = GitRepository(path, True)

    # First, we make sure the path either doesn't exist or is an  empty dir.
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception (f"{path} is not a directory!")
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception (f"{path} is not empty!")
    else:
        os.makedirs(repo.worktree)

    # Check that the repositories have been sucessfullt created
    assert repo_dir(repo, "branches", mkdir=True)
    assert repo_dir(repo, "objects", mkdir=True)
    assert repo_dir(repo, "refs", "tags", mkdir=True)
    assert repo_dir(repo, "refs", "heads", mkdir=True)

    # Create the file in .git/description
    with open(repo_file(repo, "description"), "w") as f:# type: ignore 
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    # Create the file in .git/HEAD
    with open(repo_file(repo, "HEAD"), "w") as f:       # type: ignore 
         f.write("ref: refs/heads/master\n")
    
    with open(repo_file(repo, "config"), "w") as f:     # type: ignore
          config = repo_default_config()
          config.write(f)
    
    return repo

def repo_find(path=".",required=True):
    """
    Find an existing Git repository by searching recursively up the directory tree.
    
    Parameters:
        path (str): The path from which to start searching. Defaults to current directory.
        required (bool): If True, raises an exception when no repository is found.
                        If False, returns None instead. Defaults to True.
    
    Returns:
        GitRepository: A repository object for the found Git repository.
    
    Raises:
        Exception: If required=True and no Git repository is found.
    """
    
    # Converts the provided path to a relative path (if it was not)
    path = os.path.relpath(path)

    # If .git exists in the path, return the repo object
    if os.path.isdir(os.path.join(path,".git")):
        return GitRepository(path)

    # If we haven't returned, recurse in parent, if w
    parent = os.path.realpath(os.path.join(path, ".."))

    if parent == path:
        # Bottom case
        # os.path.join("/", "..") == "/":
        # If parent==path, then path is root.
        if required:
            raise Exception("No git directory.")
        else:
            return None

    # Recursive case
    return repo_find(parent, required)

def repo_default_config():
    """ 
    Creates the repo's .config file using configparser
    """

    # Uses configparser to create an structure as the one shown here
    # [core]
    # repositoryformatversion = 0
    # filemode = false
    # bare = false

    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0")
    ret.set("core", "filemode", "false")
    ret.set("core", "bare", "false")

    return ret


