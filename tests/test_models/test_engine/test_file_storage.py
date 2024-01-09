#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    
    # ... (previous test cases)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test the get method"""
        storage = FileStorage()
        new_state = State()
        storage.new(new_state)
        storage.save()
        state_id = new_state.id

        retrieved_state = storage.get(State, state_id)
        self.assertEqual(retrieved_state, new_state)

        non_existent_state = storage.get(State, "non_existent_id")
        self.assertIsNone(non_existent_state)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test the count method"""
        storage = FileStorage()
        num_states = storage.count(State)
        self.assertEqual(num_states, 0)

        new_state = State()
        storage.new(new_state)
        storage.save()

        num_states = storage.count(State)
        self.assertEqual(num_states, 1)

        # Test count without specifying a class
        num_all_objects = storage.count()
        self.assertEqual(num_all_objects, 1)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_delete(self):
        """Test the delete method"""
        storage = FileStorage()
        new_state = State()
        storage.new(new_state)
        storage.save()
        state_id = new_state.id

        # Check that the state exists before deletion
        retrieved_state = storage.get(State, state_id)
        self.assertEqual(retrieved_state, new_state)

        # Delete the state
        storage.delete(new_state)
        storage.save()

        # Check that the state no longer exists after deletion
        deleted_state = storage.get(State, state_id)
        self.assertIsNone(deleted_state)

        # Additional test: Try to delete a non-existent state
        non_existent_state = State()
        storage.delete(non_existent_state)
        storage.save()

        # Check that deleting a non-existent state doesn't raise an error
        self.assertIsNone(storage.get(State, non_existent_state.id))

        # Additional test: Try to delete an object of a different class
        new_user = User()
        storage.new(new_user)
        storage.save()

        # Check that the user still exists after trying to delete a different class object
        retrieved_user = storage.get(User, new_user.id)
        self.assertEqual(retrieved_user, new_user)

        # Delete the user
        storage.delete(new_user)
        storage.save()

        # Check that the user no longer exists after deletion
        deleted_user = storage.get(User, new_user.id)
        self.assertIsNone(deleted_user)

# ... (remaining code)
