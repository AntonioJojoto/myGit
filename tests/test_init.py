import os
import shutil
import unittest
import tempfile
import sys
from unittest.mock import patch
import io

# Import the main command handler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mygit

class TestCommandInit(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Change to the test directory
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        # Return to the original directory
        os.chdir(self.original_dir)
        
        # Clean up the temporary directory after tests
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_init_command_default_path(self):
        """Test that 'init' command creates a repository in the current directory by default"""
        # Capture stdout to prevent print statements from showing in test output
        with patch('sys.stdout', new=io.StringIO()):
            # Run the init command with default path (current directory)
            mygit.main(["init"])
        
        # Check that .git directory was created in the current directory
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, ".git")))
    
    def test_init_command_specified_path(self):
        """Test that 'init' command creates a repository in the specified directory"""
        # Create a subdirectory
        subdir = os.path.join(self.test_dir, "subdir")
        os.makedirs(subdir)
        
        # Capture stdout to prevent print statements from showing in test output
        with patch('sys.stdout', new=io.StringIO()):
            # Run the init command with the specified path
            mygit.main(["init", subdir])
        
        # Check that .git directory was created in the specified directory
        self.assertTrue(os.path.isdir(os.path.join(subdir, ".git")))
    
    def test_init_command_nonexistent_path(self):
        """Test that 'init' command creates a repository in a non-existent directory"""
        # Define a path to a non-existent directory
        new_dir = os.path.join(self.test_dir, "new_dir")
        
        # Verify the directory doesn't exist yet
        self.assertFalse(os.path.exists(new_dir))
        
        # Capture stdout to prevent print statements from showing in test output
        with patch('sys.stdout', new=io.StringIO()):
            # Run the init command with the non-existent path
            mygit.main(["init", new_dir])
        
        # Check that the directory was created
        self.assertTrue(os.path.isdir(new_dir))
        
        # Check that .git directory was created in it
        self.assertTrue(os.path.isdir(os.path.join(new_dir, ".git")))
