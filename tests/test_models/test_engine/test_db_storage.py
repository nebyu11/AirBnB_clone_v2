#!/usr/bin/python3
"""Unittests for DBStorage class."""
import unittest
from os import getenv
from models.engine.db_storage import DBStorage
from models.state import State
from models.city import City
from models.user import User
from models import storage


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
