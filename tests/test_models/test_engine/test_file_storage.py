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


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage testing")
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

    def test_all_with_cls_str(self):
        """Test all method with string cls argument."""
        state = State()
        states = storage.all("State")
        self.assertIn("State.{}".format(state.id), states)

    def test_delete(self):
        """Test delete method."""
        state = State()
        key = "State.{}".format(state.id)
        self.assertIn(key, storage.all())
        storage.delete(state)
        self.assertNotIn(key, storage.all())

    def test_delete_none(self):
        """Test delete with None does nothing."""
        count_before = len(storage.all())
        storage.delete(None)
        self.assertEqual(len(storage.all()), count_before)

    def test_reload(self):
        """Test reload method loads objects from file.json."""
        bm = BaseModel()
        storage.new(bm)
        storage.save()
        storage.reload()
        self.assertIn("BaseModel.{}".format(bm.id), storage.all())

    def test_reload_nonexistent_file(self):
        """Test reload when file.json does not exist."""
        if os.path.exists("file.json"):
            os.remove("file.json")
        try:
            storage.reload()
        except Exception:
            self.fail("reload raised Exception on non-existent file!")

    def test_close(self):
        """Test close method calls reload."""
        bm = BaseModel()
        storage.new(bm)
        storage.save()
        storage.close()
        self.assertIn("BaseModel.{}".format(bm.id), storage.all())


if __name__ == "__main__":
    unittest.main()
