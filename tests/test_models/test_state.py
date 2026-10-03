#!/usr/bin/python3
"""Unittests for State class."""
import unittest
from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    """Test suite for State class."""

    def test_inheritance(self):
        """Test State inherits from BaseModel."""
        s = State()
        self.assertIsInstance(s, BaseModel)

    def test_attributes(self):
        """Test State default attribute values."""
        s = State()
        self.assertTrue(hasattr(s, "name"))
        self.assertEqual(s.name, "")

    def test_to_dict(self):
        """Test State to_dict method."""
        s = State()
        d = s.to_dict()
        self.assertEqual(d["__class__"], "State")

    def test_str_representation(self):
        """Test State __str__ output."""
        s = State()
        string = str(s)
        self.assertIn("[State]", string)
        self.assertIn(s.id, string)

    def test_kwargs_instantiation(self):
        """Test State instantiation with kwargs."""
        s = State(name="California")
        self.assertEqual(s.name, "California")

    def test_cities_property(self):
        """Test cities property returns a list."""
        s = State()
        self.assertIsInstance(s.cities, list)


if __name__ == "__main__":
    unittest.main()
