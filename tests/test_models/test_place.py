#!/usr/bin/python3
"""Unittests for Place class."""
import unittest
from models.place import Place
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):
    """Test suite for Place class."""

    def test_inheritance(self):
        """Test Place inherits from BaseModel."""
        p = Place()
        self.assertIsInstance(p, BaseModel)

    def test_attributes_exist(self):
        """Test Place attributes exist."""
        p = Place()
        self.assertTrue(hasattr(p, "city_id"))
        self.assertTrue(hasattr(p, "user_id"))
        self.assertTrue(hasattr(p, "name"))
        self.assertTrue(hasattr(p, "description"))
        self.assertTrue(hasattr(p, "number_rooms"))
        self.assertTrue(hasattr(p, "number_bathrooms"))
        self.assertTrue(hasattr(p, "max_guest"))
        self.assertTrue(hasattr(p, "price_by_night"))
        self.assertTrue(hasattr(p, "latitude"))
        self.assertTrue(hasattr(p, "longitude"))
        self.assertTrue(hasattr(p, "amenity_ids"))

    def test_attributes_defaults(self):
        """Test Place default attribute values."""
        p = Place()
        self.assertEqual(p.city_id, "")
        self.assertEqual(p.user_id, "")
        self.assertEqual(p.name, "")
        self.assertEqual(p.description, "")
        self.assertEqual(p.number_rooms, 0)
        self.assertEqual(p.number_bathrooms, 0)
        self.assertEqual(p.max_guest, 0)
        self.assertEqual(p.price_by_night, 0)
        self.assertEqual(p.latitude, 0.0)
        self.assertEqual(p.longitude, 0.0)
        self.assertEqual(p.amenity_ids, [])

    def test_to_dict(self):
        """Test Place to_dict method."""
        p = Place()
        d = p.to_dict()
        self.assertEqual(d["__class__"], "Place")

    def test_str_representation(self):
        """Test Place __str__ output."""
        p = Place()
        string = str(p)
        self.assertIn("[Place]", string)
        self.assertIn(p.id, string)

    def test_kwargs_instantiation(self):
        """Test Place instantiation with kwargs."""
        p = Place(name="Villa", number_rooms=3, price_by_night=150)
        self.assertEqual(p.name, "Villa")
        self.assertEqual(p.number_rooms, 3)
        self.assertEqual(p.price_by_night, 150)

    def test_amenity_ids_type(self):
        """Test amenity_ids attribute is a list."""
        p = Place()
        self.assertIsInstance(p.amenity_ids, list)


if __name__ == "__main__":
    unittest.main()
