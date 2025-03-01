import os
import zlib
import hashlib

from utils.path import repo_file
from .objects import GitBlob

def object_read(repo, sha):
    """Read object sha from Git repository repo.  Return a
    GitObject whose exact type depends on the object."""

    path = repo_file(repo, "objects", sha[0:2], sha[2:])

    if not os.path.isfile(path):  # type: ignore
        return None

    with open (path, "rb") as f:  # type: ignore
        raw = zlib.decompress(f.read())

        # Read object type
        x = raw.find(b' ')
        fmt = raw[0:x]

        # Read and validate object size
        y = raw.find(b'\x00', x)
        size = int(raw[x:y].decode("ascii"))
        if size != len(raw)-y-1:
            raise Exception(f"Malformed object {sha}: bad length")

        # Pick constructor
        match fmt:
            #case b'commit' : c=GitCommit
            #case b'tree'   : c=GitTree
            #case b'tag'    : c=GitTag
            case b'blob'   : c=GitBlob
            case _:
                raise Exception(f"Unknown type {fmt.decode("ascii")} for object {sha}")

        # Call constructor and return object
        return c(raw[y+1:])


def object_write(obj, repo=None):
    # Serialize object data
    data = obj.serialize()
    # Add header
    result = obj.fmt + b' ' + str(len(data)).encode() + b'\x00' + data
    # Compute hash
    sha = hashlib.sha1(result).hexdigest()

    if repo:
        # Compute path
        path=repo_file(repo, "objects", sha[0:2], sha[2:], mkdir=True)

        if not os.path.exists(path):    # type: ignore
            with open(path, 'wb') as f: # type: ignore
                # Compress and write
                f.write(zlib.compress(result))
    return sha
