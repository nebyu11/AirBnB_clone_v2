#!/usr/bin/python3
"""Unittests for User class."""
import unittest
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """Test suite for User class."""

    def test_inheritance(self):
        """Test User inherits from BaseModel."""
        u = User()
        self.assertIsInstance(u, BaseModel)

    def test_attributes_exist(self):
        """Test User attributes exist."""
        u = User()
        self.assertTrue(hasattr(u, "email"))
        self.assertTrue(hasattr(u, "password"))
        self.assertTrue(hasattr(u, "first_name"))
        self.assertTrue(hasattr(u, "last_name"))

    def test_attributes_defaults(self):
        """Test User default attribute values."""
        u = User()
        self.assertEqual(u.email, "")
        self.assertEqual(u.password, "")
        self.assertEqual(u.first_name, "")
        self.assertEqual(u.last_name, "")

    def test_to_dict(self):
        """Test User to_dict method."""
        u = User()
        d = u.to_dict()
        self.assertEqual(d["__class__"], "User")

    def test_str_representation(self):
        """Test User __str__ output."""
        u = User()
        string = str(u)
        self.assertIn("[User]", string)
        self.assertIn(u.id, string)

    def test_kwargs_instantiation(self):
        """Test User instantiation with kwargs."""
        u = User(email="test@user.com", first_name="John")
        self.assertEqual(u.email, "test@user.com")
        self.assertEqual(u.first_name, "John")


if __name__ == "__main__":
    unittest.main()
