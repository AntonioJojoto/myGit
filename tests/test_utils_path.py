import os
import shutil
import unittest
import tempfile

from repository.GitRepository import GitRepository
from utils.path import repo_path, repo_dir, repo_file

class TestUtilsPath(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Create a fake repo object
        self.repo = GitRepository(self.test_dir, force=True)
        
        # Create a basic .git directory structure
        os.makedirs(os.path.join(self.test_dir, ".git"))
    
    def tearDown(self):
        # Clean up the temporary directory after tests
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_repo_path(self):
        """Test that repo_path correctly computes paths under gitdir"""
        expected = os.path.join(self.test_dir, ".git", "objects")
        result = repo_path(self.repo, "objects")
        self.assertEqual(result, expected)
        
        # Test with multiple path components
        expected = os.path.join(self.test_dir, ".git", "refs", "heads", "master")
        result = repo_path(self.repo, "refs", "heads", "master")
        self.assertEqual(result, expected)
    
    def test_repo_dir_existing(self):
        """Test that repo_dir returns path for existing directories"""
        # Create a directory
        dir_path = os.path.join(self.test_dir, ".git", "objects")
        os.makedirs(dir_path)
        
        # Test that repo_dir returns the correct path
        result = repo_dir(self.repo, "objects")
        self.assertEqual(result, dir_path)
    
    def test_repo_dir_nonexistent_without_mkdir(self):
        """Test that repo_dir returns None for nonexistent dirs without mkdir"""
        result = repo_dir(self.repo, "nonexistent")
        self.assertIsNone(result)
    
    def test_repo_dir_nonexistent_with_mkdir(self):
        """Test that repo_dir creates and returns path for nonexistent dirs with mkdir"""
        dir_path = os.path.join(self.test_dir, ".git", "new_dir")
        
        # Directory should not exist yet
        self.assertFalse(os.path.exists(dir_path))
        
        # repo_dir should create it and return the path
        result = repo_dir(self.repo, "new_dir", mkdir=True)
        
        self.assertEqual(result, dir_path)
        self.assertTrue(os.path.isdir(dir_path))
    
    def test_repo_dir_fails_on_file(self):
        """Test that repo_dir raises an exception if path exists but is not a directory"""
        # Create a file
        file_path = os.path.join(self.test_dir, ".git", "not_a_dir")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write("test content")
        
        # repo_dir should raise an exception
        with self.assertRaises(Exception):
            repo_dir(self.repo, "not_a_dir")
    
    def test_repo_file(self):
        """Test that repo_file computes correct file paths"""
        # Create required parent directories
        os.makedirs(os.path.join(self.test_dir, ".git", "refs", "heads"))
        
        # Test repo_file
        expected = os.path.join(self.test_dir, ".git", "refs", "heads", "master")
        result = repo_file(self.repo, "refs", "heads", "master")
        self.assertEqual(result, expected)
    
    def test_repo_file_with_mkdir(self):
        """Test that repo_file creates parent directories if needed and mkdir=True"""
        # Test with mkdir=True
        expected = os.path.join(self.test_dir, ".git", "new", "path", "file.txt")
        result = repo_file(self.repo, "new", "path", "file.txt", mkdir=True)
        
        self.assertEqual(result, expected)
        self.assertTrue(os.path.isdir(os.path.dirname(expected)))
