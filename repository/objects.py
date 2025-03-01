class GitObject(object):
    def __init__(self, data=None):
        if data != None:
            self.deserialize(data)
        else:
            self.init()

    def serialize(self, repo):
        """This function MUST be implemented by subclasses.

        It must read the object's contents from self.data, a byte string, and
        do whatever it takes to convert it into a meaningful representation.
        What exactly that means depend on each subclass.

        """
        raise Exception("Unimplemented!")

    def deserialize(self, data):
        raise Exception("Unimplemented!")

    def init(self):
        pass # Just do nothing. This is a reasonable default!

class GitBlob(GitObject):
    fmt=b'blob'

    def serialize(self):
        """ Returns the blob data """
        return self.blobdata

    def deserialize(self, data):
        """ Stores the blob data """
        self.blobdata = data
