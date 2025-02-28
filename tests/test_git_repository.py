import os
import shutil
import unittest
import tempfile

from repository.repofun import repo_find,repo_create 
from repository.GitRepository import GitRepository



class TestGitRepository(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory after tests
         if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_repo_initilization(self):
        """Test that a repository can be initizalized"""

        # Initialize the repo in the test directory
        repo = repo_create(self.test_dir)

        # Check that the repo object is created
        self.assertIsInstance(repo,GitRepository)

        # Check that .git directory exists
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, ".git")))

        # Check that basic directories were created
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, ".git", "branches")))
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, ".git", "objects")))
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, ".git", "refs", "tags")))
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, ".git", "refs", "heads")))
        
        # Check that basic files were created
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, ".git", "HEAD")))
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, ".git", "description")))
    
    def test_repository_init_existing_directory(self):
        """Test that a repository can be initialized in an existing directory"""
        # Create a directory and a file inside it
        os.makedirs(os.path.join(self.test_dir, "subdir"))
        with open(os.path.join(self.test_dir, "test_file.txt"), "w") as f:
            f.write("test content")
        
        # Initialize a repo in the test directory
        repo = repo_create(self.test_dir)
        
        # Check that the repository was created and the file still exists
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, ".git")))
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, "test_file.txt")))
    
    def test_repository_init_fails_on_non_directory(self):
        """Test that initialization fails if path exists but is not a directory"""
        # Create a file
        file_path = os.path.join(self.test_dir, "not_a_dir")
        with open(file_path, "w") as f:
            f.write("test content")
        
        # Attempt to initialize a repo at the file's path should fail
        with self.assertRaises(Exception):
            repo_create(file_path)
    
    def test_repository_init_fails_on_existing_repo(self):
        """Test that initialization fails if the directory already contains a git repo"""
        # Initialize a repo in the test directory
        repo_create(self.test_dir)
        
        # Attempt to initialize a repo in the same directory should fail
        with self.assertRaises(Exception):
            repo_create(self.test_dir)

class TestFindRepo(unittest.TestCase):
    """ Tests if git can find repositories"""

    def setUp(self):
        # Create a temporary directory for testing
        self.git_dir = tempfile.mkdtemp()
        self.nogit_dir = tempfile.mkdtemp()

        # Create a repo 
        repo_create(self.git_dir)

    def tearDown(self):
        # Clean up the temporary directory after tests
        shutil.rmtree(self.nogit_dir)
        shutil.rmtree(self.git_dir)

    def obvious_repo(self):
        """ Test if the function is able to find a repo"""
        found_repo=repo_find(self.git_dir)
        self.assertIsInstance(found_repo,GitRepository)

    def no_repo(self):
        """ Check if no git is present, an error is raised """
        with self.assertRaises(Exception):
            repo_find(self.nogit_dir)





