import os
import shutil
import unittest
import tempfile

from repository.repofun import repo_find,repo_create 
from repository.GitRepository import GitRepository
from repository.objects import GitBlob
from repository.object_fun import object_read,object_write
from utils.path import repo_dir, repo_file, repo_path

class TestBlobRW(unittest.TestCase):
    """ 
    Test for the read and write objects functions
    Uses blobs as they have been implemented
    """
    def setUp(self):
        # Create a temporary directory for testing, also create a repo
        self.test_dir = tempfile.mkdtemp()
        self.repo = repo_create(self.test_dir)

        # Creates blobs with random data
        self.data = os.urandom(12)
        self.blob = GitBlob(self.data)



    def tearDown(self):
        # Clean up the temporary directory after tests
         if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_1_object_create(self):
        # Try to write this blob into an object in the repository
        sha =  object_write(self.blob,repo=self.repo)
        
        # Check if the folder and file has been created according to the convention of the sha
        self.assertTrue(os.path.isfile(repo_path(self.repo,"objects",sha[0:2],sha[2:])))

    def test_2_object_read(self):
        # Creates the same blob as before, just to get hash and not use the same 

        data = os.urandom(12)
        GitBlob(data)
        sha =  object_write(self.blob,repo=self.repo)

        newblob = object_read(self.repo,sha)

        # Check if the returned object is a blob
        self.assertIsInstance(newblob,GitBlob)
        self.assertEqual(newblob.serialize(),self.data)


         


