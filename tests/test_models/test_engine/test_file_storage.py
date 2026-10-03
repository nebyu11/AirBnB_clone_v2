#!/usr/bin/python3
"""Unittests for FileStorage class."""
import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class TestFileStorage(unittest.TestCase):
    """Test suite for FileStorage class."""

    def setUp(self):
        """Clean up before test."""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def tearDown(self):
        """Clean up after test."""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_all_returns_dict(self):
        """Test all method returns dictionary."""
        self.assertIsInstance(storage.all(), dict)

    def test_new_and_save(self):
        """Test new and save methods."""
        bm = BaseModel()
        u = User()
        storage.new(bm)
        storage.new(u)
        storage.save()
        self.assertTrue(os.path.exists("file.json"))
        with open("file.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("BaseModel.{}".format(bm.id), data)
        self.assertIn("User.{}".format(u.id), data)

    def test_all_with_cls(self):
        """Test all method with cls argument."""
        state = State()
        user = User()
        states = storage.all(State)
        self.assertIn("State.{}".format(state.id), states)
        self.assertNotIn("User.{}".format(user.id), states)

    def test_delete(self):
        """Test delete method."""
        state = State()
        key = "State.{}".format(state.id)
        self.assertIn(key, storage.all())
        storage.delete(state)
        self.assertNotIn(key, storage.all())


if __name__ == "__main__":
    unittest.main()
