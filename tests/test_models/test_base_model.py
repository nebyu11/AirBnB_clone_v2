#!/usr/bin/python3
"""Unittests for BaseModel class."""
import unittest
import time
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test suite for BaseModel class."""

    def test_instantiation(self):
        """Test instantiation of BaseModel."""
        bm = BaseModel()
        self.assertIsInstance(bm, BaseModel)
        self.assertIsInstance(bm.id, str)
        self.assertIsInstance(bm.created_at, datetime)
        self.assertIsInstance(bm.updated_at, datetime)

    def test_unique_id(self):
        """Test that two instances have unique ids."""
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_str_representation(self):
        """Test __str__ output."""
        bm = BaseModel()
        string = str(bm)
        self.assertIn("[BaseModel]", string)
        self.assertIn(bm.id, string)

    def test_save(self):
        """Test save method updates updated_at."""
        bm = BaseModel()
        old_updated_at = bm.updated_at
        time.sleep(0.001)
        bm.save()
        self.assertGreater(bm.updated_at, old_updated_at)

    def test_to_dict(self):
        """Test to_dict method."""
        bm = BaseModel()
        d = bm.to_dict()
        self.assertEqual(d["__class__"], "BaseModel")
        self.assertEqual(d["id"], bm.id)
        self.assertIsInstance(d["created_at"], str)
        self.assertIsInstance(d["updated_at"], str)

    def test_to_dict_type(self):
        """Test to_dict returns a dictionary."""
        bm = BaseModel()
        self.assertIsInstance(bm.to_dict(), dict)

    def test_to_dict_keys(self):
        """Test to_dict contains expected keys."""
        bm = BaseModel()
        d = bm.to_dict()
        self.assertIn("id", d)
        self.assertIn("created_at", d)
        self.assertIn("updated_at", d)
        self.assertIn("__class__", d)

    def test_kwargs_instantiation(self):
        """Test instantiation with kwargs."""
        bm = BaseModel()
        d = bm.to_dict()
        bm2 = BaseModel(**d)
        self.assertEqual(bm.id, bm2.id)
        self.assertEqual(bm.created_at, bm2.created_at)
        self.assertEqual(bm.updated_at, bm2.updated_at)

    def test_kwargs_custom_attr(self):
        """Test instantiation with custom kwargs attributes."""
        bm = BaseModel(name="Test", number=89)
        self.assertEqual(bm.name, "Test")
        self.assertEqual(bm.number, 89)

    def test_kwargs_empty(self):
        """Test instantiation with empty kwargs."""
        bm = BaseModel(**{})
        self.assertIsInstance(bm.id, str)
        self.assertIsInstance(bm.created_at, datetime)


if __name__ == "__main__":
    unittest.main()
