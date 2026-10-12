#!/usr/bin/python3
"""Unittests for DBStorage class."""
import unittest
from os import getenv
from models.engine.db_storage import DBStorage
from models.state import State
from models.city import City
from models.user import User
from models import storage


class TestDBStorageDocs(unittest.TestCase):
    """Test suite for DBStorage documentation and interface."""

    def test_module_docstring(self):
        """Test DBStorage module docstring exists."""
        import models.engine.db_storage as db_mod
        self.assertIsNotNone(db_mod.__doc__)
        self.assertGreater(len(db_mod.__doc__.strip()), 1)

    def test_class_docstring(self):
        """Test DBStorage class docstring exists."""
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertGreater(len(DBStorage.__doc__.strip()), 1)

    def test_methods_exist(self):
        """Test DBStorage methods exist."""
        self.assertTrue(hasattr(DBStorage, "all"))
        self.assertTrue(hasattr(DBStorage, "new"))
        self.assertTrue(hasattr(DBStorage, "save"))
        self.assertTrue(hasattr(DBStorage, "delete"))
        self.assertTrue(hasattr(DBStorage, "reload"))


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "DBStorage testing")
class TestDBStorage(unittest.TestCase):
    """Test suite for DBStorage."""

    def test_all_returns_dict(self):
        """Test all method returns a dictionary."""
        self.assertIsInstance(storage.all(), dict)

    def test_all_with_cls(self):
        """Test all method with class filter."""
        states = storage.all(State)
        self.assertIsInstance(states, dict)

    def test_new_and_save(self):
        """Test new and save methods."""
        state = State(name="California")
        storage.new(state)
        storage.save()
        self.assertIn("State.{}".format(state.id), storage.all(State))


if __name__ == "__main__":
    unittest.main()
