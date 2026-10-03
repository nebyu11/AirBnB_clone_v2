#!/usr/bin/python3
"""Unittests for City class."""
import unittest
from models.city import City
from models.base_model import BaseModel


class TestCity(unittest.TestCase):
    """Test suite for City class."""

    def test_inheritance(self):
        """Test City inherits from BaseModel."""
        c = City()
        self.assertIsInstance(c, BaseModel)

    def test_attributes_exist(self):
        """Test City attributes exist."""
        c = City()
        self.assertTrue(hasattr(c, "state_id"))
        self.assertTrue(hasattr(c, "name"))

    def test_attributes_defaults(self):
        """Test City default attribute values."""
        c = City()
        self.assertEqual(c.state_id, "")
        self.assertEqual(c.name, "")

    def test_to_dict(self):
        """Test City to_dict method."""
        c = City()
        d = c.to_dict()
        self.assertEqual(d["__class__"], "City")

    def test_str_representation(self):
        """Test City __str__ output."""
        c = City()
        string = str(c)
        self.assertIn("[City]", string)
        self.assertIn(c.id, string)

    def test_kwargs_instantiation(self):
        """Test City instantiation with kwargs."""
        c = City(name="San Francisco", state_id="CA123")
        self.assertEqual(c.name, "San Francisco")
        self.assertEqual(c.state_id, "CA123")


if __name__ == "__main__":
    unittest.main()
