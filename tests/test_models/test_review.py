#!/usr/bin/python3
"""Unittests for Review class."""
import unittest
from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):
    """Test suite for Review class."""

    def test_inheritance(self):
        """Test Review inherits from BaseModel."""
        r = Review()
        self.assertIsInstance(r, BaseModel)

    def test_attributes_exist(self):
        """Test Review attributes exist."""
        r = Review()
        self.assertTrue(hasattr(r, "place_id"))
        self.assertTrue(hasattr(r, "user_id"))
        self.assertTrue(hasattr(r, "text"))

    def test_attributes_defaults(self):
        """Test Review default attribute values."""
        r = Review()
        self.assertEqual(r.place_id, "")
        self.assertEqual(r.user_id, "")
        self.assertEqual(r.text, "")

    def test_to_dict(self):
        """Test Review to_dict method."""
        r = Review()
        d = r.to_dict()
        self.assertEqual(d["__class__"], "Review")

    def test_str_representation(self):
        """Test Review __str__ output."""
        r = Review()
        string = str(r)
        self.assertIn("[Review]", string)
        self.assertIn(r.id, string)

    def test_kwargs_instantiation(self):
        """Test Review instantiation with kwargs."""
        r = Review(text="Great place!", place_id="p1", user_id="u1")
        self.assertEqual(r.text, "Great place!")
        self.assertEqual(r.place_id, "p1")
        self.assertEqual(r.user_id, "u1")


if __name__ == "__main__":
    unittest.main()
