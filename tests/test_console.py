#!/usr/bin/python3
"""Unittests for console.py (HBNBCommand)."""
import unittest
from io import StringIO
import sys
import os
from console import HBNBCommand
from models import storage


class TestHBNBCommand(unittest.TestCase):
    """Test suite for HBNBCommand console."""

    def setUp(self):
        """Redirect stdout."""
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        """Restore stdout."""
        sys.stdout = sys.__stdout__
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_quit(self):
        """Test quit command."""
        cmd = HBNBCommand()
        self.assertTrue(cmd.onecmd("quit"))

    def test_EOF(self):
        """Test EOF command."""
        cmd = HBNBCommand()
        self.assertTrue(cmd.onecmd("EOF"))

    def test_create_missing_class(self):
        """Test create without class name."""
        cmd = HBNBCommand()
        cmd.onecmd("create")
        self.assertIn("** class name missing **", self.held_output.getvalue())

    def test_create_invalid_class(self):
        """Test create with invalid class name."""
        cmd = HBNBCommand()
        cmd.onecmd("create InvalidClass")
        self.assertIn("** class doesn't exist **", self.held_output.getvalue())

    def test_create_valid(self):
        """Test create with valid class."""
        cmd = HBNBCommand()
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            cmd.onecmd('create State name="California"')
            obj_id = self.held_output.getvalue().strip()
            self.assertIn("State.{}".format(obj_id), storage.all())
        else:
            cmd.onecmd("create BaseModel")
            obj_id = self.held_output.getvalue().strip()
            self.assertIn("BaseModel.{}".format(obj_id), storage.all())

    def test_show_missing_class(self):
        """Test show without class name."""
        cmd = HBNBCommand()
        cmd.onecmd("show")
        self.assertIn("** class name missing **", self.held_output.getvalue())

    def test_show_missing_id(self):
        """Test show without id."""
        cmd = HBNBCommand()
        cmd.onecmd("show BaseModel")
        self.assertIn("** instance id missing **", self.held_output.getvalue())

    def test_show_no_instance(self):
        """Test show with non-existent id."""
        cmd = HBNBCommand()
        cmd.onecmd("show BaseModel 999999")
        self.assertIn("** no instance found **", self.held_output.getvalue())

    def test_destroy_missing_class(self):
        """Test destroy without class name."""
        cmd = HBNBCommand()
        cmd.onecmd("destroy")
        self.assertIn("** class name missing **", self.held_output.getvalue())

    def test_destroy_missing_id(self):
        """Test destroy without id."""
        cmd = HBNBCommand()
        cmd.onecmd("destroy BaseModel")
        self.assertIn("** instance id missing **", self.held_output.getvalue())

    def test_all(self):
        """Test all command."""
        cmd = HBNBCommand()
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            cmd.onecmd('create State name="California"')
            self.held_output.truncate(0)
            self.held_output.seek(0)
            cmd.onecmd("all State")
            self.assertIn("[State]", self.held_output.getvalue())
        else:
            cmd.onecmd("create User")
            self.held_output.truncate(0)
            self.held_output.seek(0)
            cmd.onecmd("all User")
            self.assertIn("[User]", self.held_output.getvalue())

    def test_create_with_params(self):
        """Test create with string, float, and int parameters."""
        cmd = HBNBCommand()
        cmd.onecmd('create State name="California"')
        state_id = self.held_output.getvalue().strip()
        key = "State.{}".format(state_id)
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].name, "California")

    def test_create_with_multiple_params(self):
        """Test create with string, int, float parameters."""
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            cmd = HBNBCommand()
            cmd.onecmd('create State name="California"')
            state_id = self.held_output.getvalue().strip().split()[-1]
            self.held_output.truncate(0)
            self.held_output.seek(0)

            cmd.onecmd(
                'create City state_id="{}" name="San_Francisco"'.format(
                    state_id
                )
            )
            city_id = self.held_output.getvalue().strip().split()[-1]
            self.held_output.truncate(0)
            self.held_output.seek(0)

            cmd.onecmd('create User email="user@test.com" password="pwd"')
            user_id = self.held_output.getvalue().strip().split()[-1]
            self.held_output.truncate(0)
            self.held_output.seek(0)

            cmd.onecmd(
                'create Place city_id="{}" user_id="{}" '
                'name="My_little_house" number_rooms=4 '
                'latitude=37.773972'.format(city_id, user_id)
            )
            place_id = self.held_output.getvalue().strip().split()[-1]
            key = "Place.{}".format(place_id)
            self.assertIn(key, storage.all())
            obj = storage.all()[key]
            self.assertEqual(obj.name, "My little house")
            self.assertEqual(obj.number_rooms, 4)
            self.assertAlmostEqual(obj.latitude, 37.773972, places=3)
        else:
            cmd = HBNBCommand()
            cmd.onecmd(
                'create Place name="My_little_house" number_rooms=4 '
                'latitude=37.773972'
            )
            place_id = self.held_output.getvalue().strip()
            key = "Place.{}".format(place_id)
            self.assertIn(key, storage.all())
            obj = storage.all()[key]
            self.assertEqual(obj.name, "My little house")
            self.assertEqual(obj.number_rooms, 4)
            self.assertEqual(obj.latitude, 37.773972)

    def test_help_quit(self):
        """Test help quit."""
        cmd = HBNBCommand()
        cmd.onecmd("help quit")
        self.assertNotEqual(self.held_output.getvalue(), "")

    def test_help_EOF(self):
        """Test help EOF."""
        cmd = HBNBCommand()
        cmd.onecmd("help EOF")
        self.assertNotEqual(self.held_output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
