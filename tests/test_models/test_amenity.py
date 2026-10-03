#!/usr/bin/python3
"""Unittests for Amenity class."""
import unittest
import time
from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):
    """Test suite for Amenity class."""

    def test_inheritance(self):
        """Test Amenity inherits from BaseModel."""
        a = Amenity()
        self.assertIsInstance(a, BaseModel)

    def test_attributes(self):
        """Test Amenity default attribute values."""
        a = Amenity()
        self.assertTrue(hasattr(a, "name"))
        self.assertEqual(a.name, "")

    def test_to_dict(self):
        """Test Amenity to_dict method."""
        a = Amenity()
        d = a.to_dict()
        self.assertEqual(d["__class__"], "Amenity")

    def test_str_representation(self):
        """Test Amenity __str__ output."""
        a = Amenity()
        string = str(a)
        self.assertIn("[Amenity]", string)
        self.assertIn(a.id, string)

    def test_kwargs_instantiation(self):
        """Test Amenity instantiation with kwargs."""
        a = Amenity(name="Wifi")
        self.assertEqual(a.name, "Wifi")

    def test_save(self):
        """Test Amenity save updates updated_at."""
        a = Amenity()
        old = a.updated_at
        time.sleep(0.001)
        a.save()
        self.assertGreater(a.updated_at, old)


if __name__ == "__main__":
    unittest.main()
